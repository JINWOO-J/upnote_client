#!/usr/bin/env python3
"""
UpNote Advanced Features Usage Example
Example using latest URL scheme parameters
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

from datetime import datetime, timedelta


def advanced_note_creation():
    """Test advanced note creation features"""
    client = UpNoteClient()
    
    print("=== Advanced Note Creation Feature Test ===")
    
    # 1. Important note with color and pinning
    print("1. Creating important note (red, pinned, favorite)...")
    important_content = """# 🚨 Urgent Notice

## Server Maintenance Notice
- **Time**: January 20, 2024 (Sat) 02:00 ~ 06:00
- **Impact**: All services temporarily suspended
- **Preparation**: Data backup completed

## Checklist
{checklist}

> ⚠️ **Warning**: Services will be unavailable during maintenance hours.
""".format(
        checklist=UpNoteHelper.create_checklist([
            "Send user notification",
            "Database backup",
            "Server status monitoring",
            "Service verification after maintenance"
        ])
    )
    
    success = client.create_markdown_note(
        title="🚨 Server Maintenance Notice",
        content=important_content,
        notebook="Operations",
        tags=["urgent", "notice", "server-maintenance"],
        pinned=True,
        favorite=True,
        color="red",
        reminder="2024-01-19T18:00:00"
    )
    print(f"Important note creation: {'successful' if success else 'failed'}")
    
    # 2. Project plan note (blue)
    print("\n2. Creating project plan note (blue)...")
    project_content = """# 📋 Q1 Project Plan

## Goals
Improve user experience through new feature launch

## Key Milestones
{milestones}

## Team Composition
{team_table}

## Budget Plan
- Development: $50,000
- Marketing: $20,000
- Operations: $10,000
- **Total**: $80,000
""".format(
        milestones=UpNoteHelper.create_checklist([
            "Requirements analysis completed (1/15)",
            "UI/UX design completed (1/30)",
            "Backend API development (2/15)",
            "Frontend development (2/28)",
            "Testing and QA (3/15)",
            "Deployment and launch (3/31)"
        ]),
        team_table=UpNoteHelper.create_table(
            headers=["Role", "Person", "Experience", "Allocation"],
            rows=[
                ["PM", "Kim PM", "5 years", "100%"],
                ["Backend", "Park Dev", "3 years", "100%"],
                ["Frontend", "Lee Coder", "4 years", "100%"],
                ["Designer", "Choi Design", "2 years", "50%"],
                ["QA", "Jeong Tester", "3 years", "70%"]
            ]
        )
    )
    
    success = client.create_markdown_note(
        title="📋 Q1 Project Plan",
        content=project_content,
        notebook="Projects",
        tags=["plan", "Q1", "project"],
        color="blue",
        favorite=True
    )
    print(f"Project plan note creation: {'successful' if success else 'failed'}")
    
    # 3. Meeting note template (green)
    print("\n3. Creating meeting note template (green)...")
    meeting_template = """# 📝 Meeting Note Template

**Meeting Name**: [Meeting Title]
**Time**: [Date and Time]
**Location**: [Meeting Location/Online]
**Attendees**: [Attendee List]

## 📋 Agenda
1. [Agenda Item 1]
2. [Agenda Item 2]
3. [Agenda Item 3]

## 💬 Discussion Points
### [Agenda Item 1]
- Write discussion points

### [Agenda Item 2]
- Write discussion points

## ✅ Decisions Made
- [Decision 1]
- [Decision 2]

## 📝 Action Items
{action_items}

## 📅 Next Meeting
**Schedule**: [Next Meeting Schedule]
**Agenda**: [Next Meeting Key Agenda]
""".format(
        action_items=UpNoteHelper.create_checklist([
            "[Task Description] (Person, Due Date)",
            "[Task Description] (Person, Due Date)",
            "[Task Description] (Person, Due Date)"
        ])
    )
    
    success = client.create_markdown_note(
        title="📝 Meeting Note Template",
        content=meeting_template,
        notebook="Templates",
        tags=["template", "meeting-notes"],
        color="green"
    )
    print(f"Meeting note template creation: {'successful' if success else 'failed'}")


def test_advanced_features():
    """Test advanced features"""
    client = UpNoteClient()
    
    print("\n=== Advanced Features Test ===")
    
    # 1. Create notebook with color
    print("1. Creating notebook with color...")
    success = client.create_notebook(
        name="📊 Data Analysis",
        color="purple"
    )
    print(f"Notebook creation: {'successful' if success else 'failed'}")
    
    # 2. Create sub-notebook
    print("\n2. Creating sub-notebook...")
    success = client.create_notebook(
        name="Monthly Report",
        parent="📊 Data Analysis",
        color="yellow"
    )
    print(f"Sub-notebook creation: {'successful' if success else 'failed'}")
    
    # 3. Open notebook
    print("\n3. Opening notebook...")
    success = client.open_notebook(name="📊 Data Analysis")
    print(f"Opening notebook: {'successful' if success else 'failed'}")
    
    # 4. Advanced search (notebook and tag filtering)
    print("\n4. Running advanced search...")
    success = client.search_notes(
        query="project",
        notebook="Projects",
        tags=["plan", "important"],
        limit=10
    )
    print(f"Advanced search: {'successful' if success else 'failed'}")
    
    # 5. Open note in edit mode
    print("\n5. Opening note in edit mode...")
    success = client.open_note(
        title="📋 Q1 Project Plan",
        edit=True
    )
    print(f"Opening note in edit mode: {'successful' if success else 'failed'}")
    
    # 6. Add quick note
    print("\n6. Adding quick note...")
    quick_text = f"""
---
**{datetime.now().strftime('%Y-%m-%d %H:%M')}** Additional memo:
- New idea: AI-based automatic tag generation
- Reference link: https://example.com/ai-tagging
"""
    success = client.quick_note(
        text=quick_text,
        append=True
    )
    print(f"Adding quick note: {'successful' if success else 'failed'}")


def test_url_generation():
    """Test URL generation"""
    print("\n=== URL Generation Test ===")
    client = UpNoteClient()
    
    # Test various parameter combinations
    test_cases = [
        {
            "name": "Basic Markdown Note",
            "action": "note/new",
            "params": {
                "title": "Test Note",
                "text": "# Title\n\n**Bold Text**",
                "markdown": True,
                "tags": ["test", "markdown"]
            }
        },
        {
            "name": "Pinned Important Note",
            "action": "note/new",
            "params": {
                "title": "Important Notice",
                "text": "Important content.",
                "pinned": True,
                "favorite": True,
                "color": "red",
                "notebook": "Announcements"
            }
        },
        {
            "name": "Note with Reminder",
            "action": "note/new",
            "params": {
                "title": "Meeting Preparation",
                "text": "Meeting preparation items",
                "reminder": "2024-01-20T14:00:00",
                "tags": ["meeting", "preparation"]
            }
        },
        {
            "name": "Advanced Search",
            "action": "search",
            "params": {
                "query": "project plan",
                "notebook": "Work",
                "tags": ["important", "plan"],
                "limit": 5
            }
        }
    ]
    
    for case in test_cases:
        url = client.debug_url(case["action"], case["params"])
        print(f"\n{case['name']}:")
        print(f"URL: {url}")
        print(f"Length: {len(url)} characters")


if __name__ == "__main__":
    advanced_note_creation()
    test_advanced_features()
    test_url_generation()