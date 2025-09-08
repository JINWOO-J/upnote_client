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
        # 1. Create basic note
        print("1. Creating basic note...")
        success = client.create_note(
            text="- Write project plan\n- Attend meeting\n- Code review",
            title="Today's Tasks"
        )
        print(f"Note creation {'successful' if success else 'failed'}")
        
        # 2. Create note with detailed settings
        print("\n2. Creating note with detailed settings...")
        
        # Create checklist
        checklist_items = ["Write Python script", "Write test code", "Document"]
        checklist_content = UpNoteHelper.create_checklist(checklist_items)
        
        # Content with timestamp
        formatted_content = UpNoteHelper.format_markdown_content(
            f"# Development Tasks\n\n{checklist_content}",
            add_timestamp=True,
            add_separator=True
        )
        
        success = client.create_note(
            text=formatted_content,
            title="Development Project - UpNote URL Scheme",
            notebook="Development Projects",
            tags=["development", "Python", "URL-Scheme", "project"]
        )
        print(f"Detailed note creation {'successful' if success else 'failed'}")
        
        # 3. Create note with table
        print("\n3. Creating note with table...")
        
        # Table data
        headers = ["Task", "Assignee", "Due Date", "Status"]
        rows = [
            ["API Design", "Kim Developer", "2024-01-15", "In Progress"],
            ["UI Implementation", "Park Designer", "2024-01-20", "Pending"],
            ["Testing", "Lee Tester", "2024-01-25", "Pending"]
        ]
        
        table_content = UpNoteHelper.create_table(headers, rows)
        table_note_content = f"# Project Progress Status\n\n{table_content}"
        
        success = client.create_note(
            text=table_note_content,
            title="Project Progress Status",
            tags=["project", "status", "table"]
        )
        print(f"Table note creation {'successful' if success else 'failed'}")
        
        # 4. Create notebook
        print("\n4. Creating notebook...")
        success = client.create_notebook("New Project")
        print(f"Notebook creation {'successful' if success else 'failed'}")
        
        # 5. Search notes
        print("\n5. Searching notes...")
        success = client.search_notes("development")
        print(f"Search execution {'successful' if success else 'failed'}")
        
        # 6. Open UpNote app
        print("\n6. Opening UpNote app...")
        success = client.open_upnote()
        print(f"App opening {'successful' if success else 'failed'}")
        
        # 7. Create complex note example
        print("\n7. Creating complex note...")
        
        # Meeting note template
        meeting_content = """# Team Meeting Notes
        
**Date:** {date}
**Attendees:** Kim Developer, Park Designer, Lee Planner

## Agenda
1. Check project progress
2. Next sprint planning
3. Technical issue discussion

## Discussion Points
- Current progress: 60%
- Major completed tasks:
  - User authentication system
  - Basic UI components
  - Database schema

## Action Items
{checklist}

## Next Meeting
**Schedule:** Next Friday at 2 PM
        """.format(
            date=datetime.now().strftime("%Y-%m-%d"),
            checklist=UpNoteHelper.create_checklist([
                "Update API documentation (Kim Developer)",
                "Complete UI mockup (Park Designer)", 
                "Write test scenarios (Lee Planner)"
            ])
        )
        
        success = client.create_note(
            text=meeting_content,
            title=f"Team Meeting Notes - {datetime.now().strftime('%Y.%m.%d')}",
            notebook="Meeting Notes",
            tags=["meeting", "team", "project"]
        )
        print(f"Meeting notes creation {'successful' if success else 'failed'}")
        
    except Exception as e:
        print(f"Error occurred: {str(e)}")


def demo_url_generation():
    """URL Generation Demo"""
    print("\n=== URL Generation Demo ===")
    client = UpNoteClient()
    
    # Various URL generation examples
    examples = [
        {
            "name": "Simple note",
            "params": {"text": "Hello UpNote!"}
        },
        {
            "name": "Note with title and content",
            "params": {"title": "Test Note", "text": "This is a test."}
        },
        {
            "name": "Note with tags",
            "params": {
                "title": "Tag Test",
                "text": "Testing tag functionality.",
                "tags": ["test", "development"]
            }
        },
        {
            "name": "Note with specified notebook",
            "params": {
                "title": "Project Note",
                "text": "Project related content",
                "notebook": "Development Projects",
                "tags": ["project"]
            }
        }
    ]
    
    for example in examples:
        url = client._build_url("note/new", example["params"])
        print(f"\n{example['name']}:")
        print(f"URL: {url}")


if __name__ == "__main__":
    main()
    demo_url_generation()