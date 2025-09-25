#!/usr/bin/env python3
"""
UpNote URL Scheme Client Usage Example
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Try importing package
try:
    from upnote_python_client import UpNoteClient, UpNoteHelper
except ImportError:
    # For development environment - load module directly
    import importlib.util
    import os

    # Path to upnote_python_client/__init__.py file
    module_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
                              'upnote_python_client', '__init__.py')

    if os.path.exists(module_path):
        spec = importlib.util.spec_from_file_location("upnote_python_client", module_path)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        UpNoteClient = module.UpNoteClient
        UpNoteHelper = module.UpNoteHelper
    else:
        raise ImportError("Could not find upnote_python_client module. Please run 'pip install -e .'")

from datetime import datetime


def main():
    # Initialize UpNote client (no API key required)
    client = UpNoteClient()

    try:
        print("\n5. Searching notes...")
        success = client.search_notes("일반")
        print(f"Search execution {'successful' if success else 'failed'}")



    except Exception as e:
        print(f"Error creating notebook: {e}")

if __name__ == "__main__":
    main()
