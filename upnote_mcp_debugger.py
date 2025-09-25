#!/usr/bin/env python3
"""
MCP Server Debug Wrapper (Proxy + Tripwire)
- Proxy mode (default): spawn real server, binary passthrough (LSP/NDJSON safe),
  dump raw bytes both directions, best-effort summarize messages.
- Tripwire mode: do NOT spawn server; read the first MCP message from client,
  detect framing (NDJSON/LSP), log method/id/body, then exit (client will see disconnect).
"""

import sys
import os
import json
import subprocess
import threading
import time
import argparse
from datetime import datetime
from pathlib import Path
from typing import Optional, Tuple

# -----------------------------
# Setup paths & logs
# -----------------------------
ROOT_DIR = Path(__file__).parent
DEBUG_DIR = ROOT_DIR / "logs"
DEBUG_DIR.mkdir(exist_ok=True)
LOG_FILE = DEBUG_DIR / f"mcp_debug_{datetime.now().strftime('%Y%m%d')}.log"

BIN_IN = DEBUG_DIR / "proxy_client_to_server.bin"   # client → server
BIN_OUT = DEBUG_DIR / "proxy_server_to_client.bin"  # server → client

# -----------------------------
# Logger (stderr + file)
# -----------------------------
class Logger:
    def __init__(self, path: Path):
        self.path = path
        self.start = time.time()
        # ensure file exists
        self.path.touch(exist_ok=True)

    def log(self, cat: str, msg: str):
        elapsed = time.time() - self.start
        ts = datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")[:-3]
        line = f"[{ts}] [{elapsed:8.3f}s] [{cat:10s}] {msg}\n"
        with open(self.path, "a", encoding="utf-8") as f:
            f.write(line)
        sys.stderr.write(line)
        sys.stderr.flush()

logger = Logger(LOG_FILE)

# -----------------------------
# Helpers: framing detection & summarization
# -----------------------------
def summarize_json_bytes(prefix: str, data: bytes):
    try:
        obj = json.loads(data.decode("utf-8"))
        if isinstance(obj, dict):
            m = obj.get("method")
            i = obj.get("id")
            logger.log(prefix, f"JSON message summary: method={m!r}, id={i!r}")
        else:
            logger.log(prefix, f"JSON (non-dict) length={len(data)}")
    except Exception as e:
        logger.log(prefix, f"JSON parse failed: {e}")

def try_parse_ndjson(buffer: bytearray) -> Optional[Tuple[bytes, int]]:
    """
    If buffer contains a full NDJSON line, return (line_bytes, total_consumed).
    """
    nl = buffer.find(b"\n")
    if nl == -1:
        return None
    line = bytes(buffer[:nl+1])
    return (line.rstrip(b"\r\n"), nl+1)

def try_parse_lsp(buffer: bytearray) -> Optional[Tuple[bytes, int]]:
    """
    If buffer contains a full LSP message, return (body_bytes, total_consumed).
    """
    # Find header terminator
    sep = buffer.find(b"\r\n\r\n")
    if sep == -1:
        return None
    headers_blob = bytes(buffer[:sep+4])
    # parse headers
    headers = {}
    for raw_line in headers_blob.split(b"\r\n"):
        if not raw_line:
            continue
        if b":" in raw_line:
            k, v = raw_line.split(b":", 1)
            headers[k.strip().lower()] = v.strip()
    try:
        n = int(headers.get(b"content-length", b"0"))
    except Exception:
        n = 0
    if n <= 0:
        return None
    start = sep + 4
    if len(buffer) < start + n:
        return None
    body = bytes(buffer[start:start+n])
    return (body, start + n)

def sniff_and_summarize(prefix: str, buffer: bytearray) -> Optional[int]:
    """
    Try to parse either NDJSON or LSP message from buffer (non-destructive summary).
    Returns number of bytes consumed if a full message found, else None.
    """
    # Prefer LSP if header is present
    if buffer.startswith(b"Content-Length:") or b"\r\n\r\n" in buffer[:128]:
        lsp = try_parse_lsp(buffer)
        if lsp:
            body, consumed = lsp
            logger.log(prefix, f"LSP message detected (length={len(body)})")
            summarize_json_bytes(prefix, body)
            return consumed
    # Else, try NDJSON if starts with '{' or '['
    if buffer[:1] in (b"{", b"["):
        nd = try_parse_ndjson(buffer)
        if nd:
            line, consumed = nd
            logger.log(prefix, f"NDJSON line detected (length={len(line)})")
            summarize_json_bytes(prefix, line)
            return consumed
    return None

# -----------------------------
# Tripwire mode
# -----------------------------
def run_tripwire():
    logger.log("STARTUP", f"TRIPWIRE mode ON. Logging first client message then exit.")
    logger.log("ENV", f"exe: {sys.executable}")
    logger.log("ENV", f"cwd: {os.getcwd()}")
    logger.log("ENV", f"PATH: {os.environ.get('PATH')}")
    logger.log("ENV", f"PYTHONPATH: {os.environ.get('PYTHONPATH')}")

    # read some bytes to detect framing
    buf = bytearray()
    sys.stdin.buffer.flush()
    # Read with small timeout-like behavior: read chunks until we see a message
    # (since we can't set non-blocking cleanly here, just read a chunk; most clients send immediately)
    chunk = sys.stdin.buffer.readline()  # good for NDJSON and first LSP header line
    if chunk:
        buf.extend(chunk)
        # If it looks like LSP, read rest of headers and body
        consumed = sniff_and_summarize("INPUT", buf)
        if consumed is None:
            # Read more in case of LSP body
            more = sys.stdin.buffer.read1(8192) if hasattr(sys.stdin.buffer, "read1") else sys.stdin.buffer.read(8192)
            if more:
                buf.extend(more)
                consumed = sniff_and_summarize("INPUT", buf)
        if consumed is None:
            # fallback: log raw
            logger.log("INPUT", f"Raw first bytes ({len(buf)}): {buf[:256]!r}")
    else:
        logger.log("INPUT", "No bytes from client (EOF?)")

    logger.log("COMPLETE", f"Tripwire captured. Exiting now (client likely sees disconnect).")

# -----------------------------
# Proxy mode: spawn real server and tee bytes
# -----------------------------
def pump(src, dst, tap_path: Path, prefix: str):
    """
    Binary pump: read chunks from src, write to dst, tee to tap file, and try to summarize messages.
    """
    tap = open(tap_path, "wb")
    buf = bytearray()
    try:
        while True:
            data = src.read(1)
            if not data:
                break
            dst.write(data)
            dst.flush()
            tap.write(data)
            tap.flush()

            # accumulate and attempt to summarize full messages (best-effort)
            buf.extend(data)
            consumed = sniff_and_summarize(prefix, buf)
            if consumed:
                # drop consumed bytes
                del buf[:consumed]
                # In case multiple messages queued, try again quickly
                consumed2 = sniff_and_summarize(prefix, buf)
                if consumed2:
                    del buf[:consumed2]
    except Exception as e:
        logger.log("ERROR", f"Pump error [{prefix}]: {e}")
    finally:
        tap.close()

def run_proxy(server_script: Path):
    # Spawn real server (binary stdio!)
    cmd = [sys.executable, str(server_script)]
    logger.log("STARTUP", f"Proxy mode: launching server: {' '.join(cmd)}")
    try:
        proc = subprocess.Popen(
            cmd,
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            bufsize=0,      # unbuffered
            text=False,     # binary mode
            env={**os.environ, "PYTHONUNBUFFERED": "1"}
        )
        logger.log("STARTUP", f"Server PID: {proc.pid}")
    except Exception as e:
        logger.log("ERROR", f"Failed to start server process: {e}")
        sys.exit(1)

    # Mirror server stderr to our stderr (text decode best-effort)
    def mirror_stderr():
        try:
            while True:
                line = proc.stderr.readline()
                if not line:
                    break
                try:
                    s = line.decode("utf-8", "replace").rstrip()
                except Exception:
                    s = repr(line)
                logger.log("STDERR", s)
        except Exception as e:
            logger.log("ERROR", f"stderr mirror error: {e}")

    t_err = threading.Thread(target=mirror_stderr, daemon=True)
    t_err.start()

    # Start pumps
    t_c2s = threading.Thread(
        target=pump,
        args=(sys.stdin.buffer, proc.stdin, BIN_IN, "C→S"),
        daemon=True,
    )
    t_s2c = threading.Thread(
        target=pump,
        args=(proc.stdout, sys.stdout.buffer, BIN_OUT, "S→C"),
        daemon=True,
    )
    t_c2s.start()
    t_s2c.start()

    # wait for process
    try:
        ret = proc.wait()
        logger.log("SHUTDOWN", f"Server exited with code {ret}")
    except KeyboardInterrupt:
        logger.log("SHUTDOWN", "KeyboardInterrupt; terminating server")
        try:
            proc.terminate()
            proc.wait(timeout=5)
        except Exception:
            proc.kill()
            proc.wait()


def main():
    ap = argparse.ArgumentParser(description="MCP Debug Wrapper (proxy + tripwire)")
    ap.add_argument("--mode", choices=["proxy", "tripwire"], default=os.environ.get("MCP_WRAPPER_MODE", "proxy"))
    ap.add_argument("--server",
                    default=os.environ.get("MCP_WRAPPER_SERVER", str(ROOT_DIR / "upnote_mcp_server.py")),
                    help="Path to the real MCP server script (proxy mode only)")
    args = ap.parse_args()

    logger.log("STARTUP", f"Debug wrapper started, logging to: {LOG_FILE}")
    logger.log("STARTUP", f"Mode: {args.mode}")
    logger.log("STARTUP", f"Python: {sys.version}")
    logger.log("STARTUP", f"Working dir: {os.getcwd()}")
    logger.log("STARTUP", f"Script dir: {ROOT_DIR}")
    logger.log("STARTUP", f"PATH: {os.environ.get('PATH')}")
    logger.log("STARTUP", f"PYTHONPATH: {os.environ.get('PYTHONPATH')}")

    if args.mode == "proxy":
        server_script = Path(args.server)
        if not server_script.exists():
            logger.log("ERROR", f"Server script not found: {server_script}")
            sys.exit(1)
        logger.log("STARTUP", f"Server script found: {server_script}")
        run_proxy(server_script)
    else:
        run_tripwire()

    # tail note
    sys.stderr.write("\n" + "="*60 + "\n")
    sys.stderr.write(f"Debug session complete.\n")
    sys.stderr.write(f"Log file: {LOG_FILE}\n")
    sys.stderr.write(f"Binary dumps: {BIN_IN}, {BIN_OUT}\n")
    sys.stderr.write("="*60 + "\n")

if __name__ == "__main__":
    main()
