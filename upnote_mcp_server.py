#!/usr/bin/env python3
"""
UpNote MCP Server — stdio (Dual framing: LSP + NDJSON)

- 프레이밍: 첫 입력 라인으로 NDJSON/LSP 자동 감지 → 동일 모드로 응답
- 알림(notification, id 없음)은 응답 없이 처리 (대기 금지)
- initialize 응답은 SDK와 최대한 호환(capabilities/prompts/resources/tools/experimental)
- stdout: 프로토콜 메시지 전용, stderr: 로깅 전용
"""

import sys
import os
import json
import logging
from typing import Optional, Dict, Any, List

# -------------------------
# Logging (stderr only)
# -------------------------
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[logging.StreamHandler(sys.stderr)],
)
log = logging.getLogger("upnote-mcp-server")

# -------------------------
# Optional UpNote client import (fail-soft)
# -------------------------
# sys.path.insert(0, os.path.join(os.path.dirname(__file__), "upnote_client"))
UPNOTE_OK = True
UpNoteClient = None
try:
    from upnote_python_client import UpNoteClient  # type: ignore
    log.info("UpNoteClient import OK")
except Exception as e:
    UPNOTE_OK = False
    log.warning(f"UpNoteClient import failed; tools will return errors on call: {e}")

# -------------------------
# Transport: dual framing
# -------------------------
TRANSPORT_MODE: Optional[str] = None  # "ndjson" | "lsp"

def _write_lsp(payload: Dict[str, Any]) -> None:
    body = json.dumps(payload, ensure_ascii=False, separators=(",", ":")).encode("utf-8")
    header = f"Content-Length: {len(body)}\r\n\r\n".encode("ascii")
    sys.stdout.buffer.write(header)
    sys.stdout.buffer.write(body)
    sys.stdout.buffer.flush()

def _write_ndjson(payload: Dict[str, Any]) -> None:
    text = json.dumps(payload, ensure_ascii=False, separators=(",", ":")) + "\n"
    sys.stdout.write(text)
    sys.stdout.flush()

def write_message(payload: Dict[str, Any]) -> None:
    if TRANSPORT_MODE == "lsp":
        _write_lsp(payload)
    else:
        _write_ndjson(payload)

def write_result(id_value: Any, result: Any) -> None:
    write_message({"jsonrpc": "2.0", "id": id_value, "result": result})

def write_error(id_value: Any, code: int, message: str) -> None:
    write_message({"jsonrpc": "2.0", "id": id_value, "error": {"code": code, "message": message}})

def _read_lsp_from(first_line: bytes) -> Optional[Dict[str, Any]]:
    headers: Dict[str, str] = {}
    def add_header(line: bytes):
        try:
            k, v = line.decode("ascii").split(":", 1)
            headers[k.strip().lower()] = v.strip()
        except Exception:
            pass

    if first_line not in (b"\r\n", b"\n"):
        add_header(first_line)
    # read until blank
    while True:
        line = sys.stdin.buffer.readline()
        if not line:
            return None
        if line in (b"\r\n", b"\n"):
            break
        add_header(line)

    try:
        n = int(headers.get("content-length", "0"))
    except ValueError:
        n = 0
    if n <= 0:
        log.error("Invalid Content-Length")
        return None

    body = sys.stdin.buffer.read(n)
    if not body or len(body) != n:
        log.error("Unexpected EOF reading LSP body")
        return None

    try:
        return json.loads(body.decode("utf-8"))
    except Exception as e:
        log.error(f"Failed to parse LSP JSON: {e}")
        return None

def _read_ndjson_from(first_line: bytes) -> Optional[Dict[str, Any]]:
    try:
        return json.loads(first_line.decode("utf-8").strip())
    except Exception as e:
        log.error(f"Failed to parse NDJSON: {e}")
        return None

def read_message() -> Optional[Dict[str, Any]]:
    """Auto-detect framing from the first non-empty line."""
    global TRANSPORT_MODE
    first_line = sys.stdin.buffer.readline()
    if not first_line:
        return None
    stripped = first_line.lstrip()
    if stripped.startswith(b"{") or stripped.startswith(b"["):
        TRANSPORT_MODE = TRANSPORT_MODE or "ndjson"
        return _read_ndjson_from(first_line)
    else:
        TRANSPORT_MODE = TRANSPORT_MODE or "lsp"
        return _read_lsp_from(first_line)

# -------------------------
# MCP core handlers
# -------------------------
SERVER_INFO = {
    "name": "upnote-mcp",
    "version": "1.0.0",
    "description": "MCP server for UpNote integration (stdio)",
}

def resp_initialize(params: Dict[str, Any]) -> Dict[str, Any]:
    client_protocol = params.get("protocolVersion", "1.0.0")
    if isinstance(client_protocol, str) and client_protocol.startswith("202"):
        protocol_version = client_protocol
    else:
        protocol_version = "1.0.0"

    # Align with SDK-style shape
    return {
        "protocolVersion": protocol_version,
        "capabilities": {
            "experimental": {},
            "prompts": {"listChanged": False},
            "resources": {"subscribe": False, "listChanged": False},
            "tools": {"listChanged": False},
        },
        "serverInfo": {
            "name": SERVER_INFO["name"],
            # SDK는 자체 버전 표시를 하기도 하지만 여기선 서버 버전만 표기
            "version": SERVER_INFO["version"],
        },
    }

def list_tools() -> Dict[str, Any]:
    tools: List[Dict[str, Any]] = [
        {
            "name": "create_note",
            "description": "Create a new note in UpNote",
            "inputSchema": {
                "type": "object",
                "properties": {
                    "title": {"type": "string"},
                    "text": {"type": "string"},
                    "notebook": {"type": "string"},
                    "tags": {"type": "array", "items": {"type": "string"}},
                    "pinned": {"type": "boolean"},
                    "favorite": {"type": "boolean"},
                },
                "required": ["title", "text"],
            },
        },
        {
            "name": "create_markdown_note",
            "description": "Create a markdown formatted note in UpNote",
            "inputSchema": {
                "type": "object",
                "properties": {
                    "title": {"type": "string"},
                    "content": {"type": "string"},
                    "notebook": {"type": "string"},
                    "tags": {"type": "array", "items": {"type": "string"}},
                    "add_timestamp": {"type": "boolean"},
                },
                "required": ["title", "content"],
            },
        },
        {
            "name": "create_task_note",
            "description": "Create a task list note in UpNote",
            "inputSchema": {
                "type": "object",
                "properties": {
                    "title": {"type": "string"},
                    "tasks": {"type": "array", "items": {"type": "string"}},
                    "notebook": {"type": "string"},
                    "due_date": {"type": "string"},
                    "priority": {"type": "string", "enum": ["low", "medium", "high"]},
                },
                "required": ["title", "tasks"],
            },
        },
        {
            "name": "create_meeting_note",
            "description": "Create a meeting note in UpNote",
            "inputSchema": {
                "type": "object",
                "properties": {
                    "title": {"type": "string"},
                    "date": {"type": "string"},
                    "attendees": {"type": "array", "items": {"type": "string"}},
                    "agenda": {"type": "string"},
                    "notebook": {"type": "string"},
                    "location": {"type": "string"},
                },
                "required": ["title", "date"],
            },
        },
        {
            "name": "create_project_note",
            "description": "Create a project note in UpNote",
            "inputSchema": {
                "type": "object",
                "properties": {
                    "project_name": {"type": "string"},
                    "description": {"type": "string"},
                    "milestones": {"type": "array", "items": {"type": "string"}},
                    "team_members": {"type": "array", "items": {"type": "string"}},
                    "due_date": {"type": "string"},
                    "priority": {"type": "string", "enum": ["low", "medium", "high"]},
                },
                "required": ["project_name", "description"],
            },
        },
        # {
        #     "name": "create_daily_note",
        #     "description": "Create a daily journal note in UpNote",
        #     "inputSchema": {
        #         "type": "object",
        #         "properties": {
        #             "date": {"type": "string"},
        #             "mood": {"type": "string"},
        #             "weather": {"type": "string"},
        #             "goals": {"type": "array", "items": {"type": "string"}},
        #             "reflections": {"type": "string"},
        #         },
        #         "required": ["date"],
        #     },
        # },
        {
            "name": "search_notes",
            "description": "Search for notes in UpNote",
            "inputSchema": {
                "type": "object",
                "properties": {
                    "query": {"type": "string"},
                    "notebook": {"type": "string"},
                    "tags": {"type": "array", "items": {"type": "string"}},
                    "limit": {"type": "integer"},
                },
                "required": ["query"],
            },
        },
        {
            "name": "open_note",
            "description": "Open a specific note in UpNote",
            "inputSchema": {
                "type": "object",
                "properties": {
                    "note_id": {"type": "string"},
                    "title": {"type": "string"},
                    "edit": {"type": "boolean"},
                },
            },
        },
        {
            "name": "create_notebook",
            "description": "Create a new notebook in UpNote",
            "inputSchema": {
                "type": "object",
                "properties": {
                    "title": {"type": "string"},
                    "color": {"type": "string"},
                    "parent": {"type": "string"},
                },
                "required": ["title"],
            },
        },
        {
            "name": "open_notebook",
            "description": "Open a notebook in UpNote",
            "inputSchema": {
                "type": "object",
                "properties": {
                    "name": {"type": "string"},
                    "notebook_id": {"type": "string"},
                },
            },
        },
        {
            "name": "open_upnote",
            "description": "Open the UpNote application",
            "inputSchema": {"type": "object", "properties": {}},
        },
        {
            "name": "import_note",
            "description": "Import a note into UpNote",
            "inputSchema": {
                "type": "object",
                "properties": {
                    "path": {"type": "string"},
                    "notebook": {"type": "string"},
                    "tags": {"type": "array", "items": {"type": "string"}},
                },
                "required": ["path"],
            },
        },
        {
            "name": "export_note",
            "description": "Export a note from UpNote",
            "inputSchema": {
                "type": "object",
                "properties": {
                    "note_id": {"type": "string"},
                    "format": {"type": "string", "enum": ["md", "html", "pdf"]},
                    "dest_path": {"type": "string"},
                },
                "required": ["note_id", "format", "dest_path"],
            },
        },
    ]
    return {"tools": tools}

def call_tool(params: Dict[str, Any]) -> Dict[str, Any]:
    name = params.get("name")
    args = params.get("arguments", {}) or {}
    log.info(f"tools/call: {name}")

    if not UPNOTE_OK or UpNoteClient is None:
        return {
            "content": [{"type": "text", "text": json.dumps({"success": False, "error": "UpNote client not available"})}],
            "isError": True,
        }

    try:
        client = UpNoteClient()
    except Exception as e:
        return {
            "content": [{"type": "text", "text": json.dumps({"success": False, "error": f"Failed to init client: {e}"})}],
            "isError": True,
        }

    try:
        if name == "create_note":
            res = client.create_note(**args)
        elif name == "create_markdown_note":
            res = client.create_markdown_note(**args)
        elif name == "create_task_note":
            res = client.create_task_note(**args)
        elif name == "create_meeting_note":
            res = client.create_meeting_note(**args)
        elif name == "create_project_note":
            res = client.create_project_note(**args)
        elif name == "create_daily_note":
            res = client.create_daily_note(**args)
        elif name == "search_notes":
            res = client.search_notes(**args)
        elif name == "open_note":
            res = client.open_note(**args)
        elif name == "create_notebook":
            res = client.create_notebook(**args)
        elif name == "open_notebook":
            res = client.open_notebook(**args)
        # elif name == "quick_note":
        #     res = client.quick_note(**args)
        elif name == "open_upnote":
            res = client.open_upnote(**args)
        elif name == "import_note":
            res = client.import_note(**args)
        elif name == "export_note":
            res = client.export_note(**args)
        else:
            return {
                "content": [{"type": "text", "text": json.dumps({"success": False, "error": f"Unknown tool: {name}"})}],
                "isError": True,
            }

        return {
            "content": [{"type": "text", "text": json.dumps({"success": True, "result": res})}],
            "isError": False,
        }

    except Exception as e:
        return {
            "content": [{"type": "text", "text": json.dumps({"success": False, "error": str(e)})}],
            "isError": True,
        }

# -------------------------
# Main loop
# -------------------------
def main():
    log.info("Starting UpNote MCP Server (stdio, dual framing)")
    while True:
        req = read_message()
        if req is None:
            log.info("EOF / invalid; exiting")
            break

        method = req.get("method")
        req_id = req.get("id")

        # Notifications: no response
        if req_id is None:
            # Best-effort side effects or logging only
            continue

        try:
            if method == "initialize":
                params = req.get("params", {}) or {}
                result = resp_initialize(params)
                write_result(req_id, result)
            elif method == "tools/list":
                write_result(req_id, list_tools())
            elif method == "tools/call":
                params = req.get("params", {}) or {}
                write_result(req_id, call_tool(params))
            elif method == "ping":
                # SDK는 빈 result로 응답
                write_result(req_id, {})
            elif method == "shutdown":
                write_result(req_id, {})
                break
            else:
                write_error(req_id, -32601, f"Method not found: {method}")
        except Exception as e:
            log.exception("Error handling request")
            write_error(req_id, -32603, f"Internal error: {e}")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        pass
