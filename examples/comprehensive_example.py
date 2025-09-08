#!/usr/bin/env python3
"""
UpNote Comprehensive Feature Example
Example showing extended parameters and special note creation features
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


def test_extended_parameters():
    """Test extended parameters"""
    client = UpNoteClient()
    
    print("=== Extended Parameters Test ===")
    
    # 1. Complex note using all parameters
    print("1. Creating complex note with all parameters...")
    
    comprehensive_content = """# 🚀 Project Kickoff Meeting

## Project Overview
New AI-based note app development project

## Key Features
- Automatic tag generation
- Smart search
- Voice recognition
- Multilingual support

## Tech Stack
{tech_stack}

## Schedule
{schedule}

## Team Roles
{team_roles}

## Budget Plan
- Development: $100,000
- Marketing: $50,000
- Operations: $30,000
- **Total**: $180,000

## Risk Factors
- Technical complexity
- Market competition
- Staff shortage

## Success Metrics
- 10,000 users achieved
- App Store rating above 4.5
- Monthly revenue of $10,000 achieved
""".format(
        tech_stack=UpNoteHelper.create_table(
            headers=["Area", "Technology", "Version", "Person"],
            rows=[
                ["Frontend", "React Native", "0.72", "Kim Mobile"],
                ["Backend", "Node.js", "18.17", "Park Server"],
                ["Database", "MongoDB", "6.0", "Lee DB"],
                ["AI/ML", "TensorFlow", "2.13", "Choi AI"],
                ["Cloud", "AWS", "Latest", "Jeong Cloud"]
            ]
        ),
        schedule=UpNoteHelper.create_checklist([
            "Requirements analysis (Week 1)",
            "System design (Weeks 2-3)",
            "Prototype development (Weeks 4-6)",
            "MVP development (Weeks 7-12)",
            "Beta testing (Weeks 13-14)",
            "Official launch (Week 15)"
        ]),
        team_roles=UpNoteHelper.create_table(
            headers=["Name", "Role", "Experience", "Responsibility"],
            rows=[
                ["Kim Team Lead", "Project Manager", "10 years", "Overall management"],
                ["Park Developer", "Lead Developer", "8 years", "Architecture design"],
                ["Lee Design", "UI/UX Designer", "5 years", "User experience"],
                ["Choi Marketing", "Marketing", "6 years", "Market analysis"],
                ["Jeong QA", "QA Engineer", "4 years", "Quality assurance"]
            ]
        )
    )
    
    success = client.create_note(
        text=comprehensive_content,
        title="🚀 AI Note App Project Kickoff",
        notebook="Project Management",
        folder="2024/Q1",
        tags=["project", "kickoff", "AI", "mobile-app"],
        category="work",
        markdown=True,
        pinned=True,
        favorite=True,
        starred=True,
        color="blue",
        priority="high",
        due_date="2024-06-30",
        reminder="2024-01-22T09:00:00",
        author="Project Manager",
        source="Kickoff Meeting",
        url="https://company.com/projects/ai-note-app",
        shared=True,
        format="markdown",
        encoding="utf-8"
    )
    print(f"Complex note creation: {'successful' if success else 'failed'}")
    
    # 2. Encrypted confidential note
    print("\n2. Creating encrypted confidential note...")
    
    confidential_content = """# 🔒 Confidential Information

## Server Access Information
- **Host**: production.company.com
- **User**: admin
- **Port**: 22

## API Keys
- **OpenAI**: sk-...
- **AWS**: AKIA...
- **Stripe**: pk_live_...

## Database Information
- **Connection String**: mongodb://...
- **Backup Location**: s3://backups/...

⚠️ **Warning**: Do not share this information externally.
"""
    
    success = client.create_note(
        text=confidential_content,
        title="🔒 Server and API Information",
        notebook="Confidential",
        tags=["confidential", "server", "API", "security"],
        color="red",
        encrypted=True,
        password="secure123!",
        readonly=False,
        shared=False,
        public=False,
        priority="urgent"
    )
    print(f"Confidential note creation: {'successful' if success else 'failed'}")
    
    # 3. Travel note with location information
    print("\n3. Creating travel note with location information...")
    
    travel_content = """# ✈️ Jeju Island Travel Plan

## Travel Schedule
**Period**: March 15-18, 2024 (3 nights 4 days)

## Accommodation Information
- **Hotel**: Jeju Shilla Hotel
- **Address**: Jeju Special Self-Governing Province Jeju City Yeondong
- **Check-in**: 15:00
- **Check-out**: 11:00

## Places to Visit
{places}

## Restaurant List
{restaurants}

## Packing List
{packing_list}

## Budget
- Airfare: 400,000 KRW
- Accommodation: 600,000 KRW
- Food: 300,000 KRW
- Tourism: 200,000 KRW
- **Total Budget**: 1,500,000 KRW
""".format(
        places=UpNoteHelper.create_checklist([
            "Seongsan Ilchulbong (Sunrise viewing)",
            "Hallasan National Park (Hiking)",
            "Udo (Bicycle tour)",
            "Cheonjiyeon Waterfall (Walking)",
            "Hyeopjae Beach (Beach relaxation)",
            "Jeju Folk Village (Cultural experience)"
        ]),
        restaurants=UpNoteHelper.create_table(
            headers=["Restaurant", "Food", "Location", "Budget"],
            rows=[
                ["Black Pork Restaurant", "Black Pork BBQ", "Jeju City", "50,000 KRW"],
                ["Haenyeo's House", "Abalone Porridge", "Seongsan", "30,000 KRW"],
                ["Olle Noodles", "Meat Noodles", "Seogwipo", "15,000 KRW"],
                ["Cafe Del Mundo", "Coffee", "Aewol", "20,000 KRW"]
            ]
        ),
        packing_list=UpNoteHelper.create_checklist([
            "Passport/ID",
            "Printed flight tickets",
            "Camera and charger",
            "Comfortable shoes (hiking boots)",
            "Sunscreen and hat",
            "Umbrella (weather preparation)"
        ])
    )
    
    success = client.create_note(
        text=travel_content,
        title="✈️ Jeju Island Travel Plan",
        notebook="Travel",
        tags=["travel", "Jeju Island", "vacation", "plan"],
        color="green",
        location="Jeju Special Self-Governing Province",
        due_date="2024-03-15",
        reminder="2024-03-10T10:00:00",
        attachments=["flight_ticket.pdf", "hotel_reservation.pdf"],
        template="travel"
    )
    print(f"Travel note creation: {'successful' if success else 'failed'}")


def test_special_note_types():
    """Test special note types"""
    client = UpNoteClient()
    
    print("\n=== Special Note Types Test ===")
    
    # 1. Task note
    print("1. Creating task note...")
    success = client.create_task_note(
        title="Weekly Work Plan",
        tasks=[
            "Write project proposal",
            "Prepare client meeting",
            "Complete code review",
            "Update documentation",
            "Attend team meeting"
        ],
        notebook="Work",
        due_date="2024-01-26",
        priority="high",
        tags=["work", "weekly-plan"],
        reminder="2024-01-22T09:00:00"
    )
    print(f"Task note creation: {'successful' if success else 'failed'}")
    
    # 2. Meeting note
    print("\n2. Creating meeting note...")
    success = client.create_meeting_note(
        title="Q1 Strategic Meeting",
        date="January 25, 2024 (Thu) 14:00",
        attendees=["CEO Kim", "Director Park", "Manager Lee", "Team Lead Choi"],
        agenda=[
            "Q4 performance review",
            "Q1 goal setting",
            "New project discussion",
            "Budget plan approval"
        ],
        notebook="Meeting Notes",
        location="Head Office Conference Room",
        tags=["strategic-meeting", "Q1", "executive"]
    )
    print(f"Meeting note creation: {'successful' if success else 'failed'}")
    
    # 3. Project note
    print("\n3. Creating project note...")
    success = client.create_project_note(
        project_name="Mobile App Renewal",
        description="A project to improve the UI/UX of the existing mobile app and add new features",
        milestones=[
            "User research completed",
            "Wireframe design",
            "UI design completion",
            "Frontend development",
            "Backend API integration",
            "Testing and QA",
            "App Store deployment"
        ],
        team_members=[
            "Kim Planner (Planner)",
            "Park Design (UI/UX Designer)",
            "Lee Developer (Frontend Developer)",
            "Choi Server (Backend Developer)",
            "Jeong Test (QA Engineer)"
        ],
        due_date="2024-06-30",
        notebook="Projects",
        priority="high"
    )
    print(f"Project note creation: {'successful' if success else 'failed'}")
    
    # 4. Daily note
    print("\n4. Creating daily note...")
    success = client.create_daily_note(
        mood="😊 Good",
        weather="☀️ Sunny",
        goals=[
            "Exercise for 30 minutes",
            "Read for 1 hour",
            "Organize project progress",
            "Dinner with family"
        ],
        reflections="Today was a fun day learning new technology. UpNote API automation was particularly useful.",
        notebook="Diary"
    )
    print(f"Daily note creation: {'successful' if success else 'failed'}")


def test_url_debugging():
    """URL generation debugging"""
    print("\n=== URL Debugging ===")
    client = UpNoteClient()
    
    # Test complex parameter combinations
    complex_params = {
        "title": "Complex Note Test",
        "text": "# Title\n\n**Bold text** and *italic*\n\n- List 1\n- List 2",
        "notebook": "Test Notebook",
        "tags": ["test", "complex", "debugging"],
        "markdown": True,
        "pinned": True,
        "favorite": True,
        "color": "purple",
        "priority": "high",
        "reminder": "2024-01-25T15:30:00",
        "location": "Seoul Gangnam-gu",
        "author": "Tester",
        "encrypted": False,
        "shared": True,
        "format": "markdown"
    }
    
    url = client.debug_url("note/new", complex_params)
    print(f"\nComplex parameter URL:")
    print(f"Length: {len(url)} characters")
    print(f"URL: {url[:100]}..." if len(url) > 100 else f"URL: {url}")
    
    # Test simple parameters
    simple_params = {
        "title": "Simple Note",
        "text": "Simple content",
        "markdown": True
    }
    
    simple_url = client.debug_url("note/new", simple_params)
    print(f"\nSimple parameter URL:")
    print(f"URL: {simple_url}")


if __name__ == "__main__":
    test_extended_parameters()
    test_special_note_types()
    test_url_debugging()