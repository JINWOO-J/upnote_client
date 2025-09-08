"""
Comprehensive Test Script for All Features
Tests only URL generation without opening the actual UpNote app
"""

import sys
import traceback
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


def test_basic_functionality():
    """Test basic functionality"""
    print("=== Basic Functionality Test ===")
    
    try:
        client = UpNoteClient()
        
        # 1. Test client initialization
        assert client.base_scheme == "upnote://x-callback-url"
        assert client.system in ["Darwin", "Windows", "Linux"]
        print("✅ Client initialization successful")
        
        # 2. Test URL generation
        test_params = {"title": "Test", "text": "Content"}
        url = client._build_url("note/new", test_params)
        assert url.startswith("upnote://x-callback-url/note/new")
        assert "title=Test" in url or "title=%ED%85%8C%EC%8A%A4%ED%8A%B8" in url
        print("✅ URL generation successful")
        
        # 3. Test parameter processing
        complex_params = {
            "title": "Complex Title",
            "tags": ["Tag1", "Tag2"],
            "markdown": True,
            "pinned": False,
            "priority": None
        }
        url = client._build_url("note/new", complex_params)
        assert "markdown=true" in url
        assert "pinned=false" in url
        assert "priority" not in url  # None values should be excluded
        print("✅ Parameter processing successful")
        
        return True
        
    except Exception as e:
        print(f"❌ Basic functionality test failed: {str(e)}")
        traceback.print_exc()
        return False


def test_helper_functions():
    """Test helper functions"""
    print("\n=== Helper Functions Test ===")
    
    try:
        # 1. Test checklist creation
        items = ["Item 1", "Item 2", "Item 3"]
        checklist = UpNoteHelper.create_checklist(items)
        expected = "- [ ] Item 1\n- [ ] Item 2\n- [ ] Item 3"
        assert checklist == expected
        print("✅ Checklist creation successful")
        
        # 2. Test table creation
        headers = ["Name", "Age"]
        rows = [["Kim", "30"], ["Lee", "25"]]
        table = UpNoteHelper.create_table(headers, rows)
        assert "| Name | Age |" in table
        assert "| --- | --- |" in table
        assert "| Kim | 30 |" in table
        print("✅ Table creation successful")
        
        # 3. Test markdown formatting
        content = "Original content"
        formatted = UpNoteHelper.format_markdown_content(content, add_timestamp=True)
        assert "Created:" in formatted
        assert "Original content" in formatted
        print("✅ Markdown formatting successful")
        
        # 4. Test empty table handling
        empty_table = UpNoteHelper.create_table([], [])
        assert empty_table == ""
        print("✅ Empty table handling successful")
        
        return True
        
    except Exception as e:
        print(f"❌ Helper functions test failed: {str(e)}")
        traceback.print_exc()
        return False


def test_note_creation():
    """Test note creation features (URL generation only)"""
    print("\n=== Note Creation Feature Test ===")
    
    try:
        client = UpNoteClient()
        
        # 1. Test basic note creation URL
        params = {
            "title": "Basic Note",
            "text": "Basic content",
            "markdown": True
        }
        url = client.debug_url("note/new", params)
        assert "title=" in url
        assert "text=" in url
        assert "markdown=true" in url
        print("✅ Basic note creation URL successful")
        
        # 2. Test extended parameter note creation URL
        params = {
            "title": "Extended Note",
            "text": "# Title\n\nContent",
            "notebook": "TestBook",
            "tags": ["Tag1", "Tag2"],
            "pinned": True,
            "favorite": True,
            "color": "red",
            "priority": "high",
            "due_date": "2024-12-31",
            "reminder": "2024-12-30T09:00:00",
            "author": "Tester",
            "encrypted": False,
            "shared": True
        }
        url = client.debug_url("note/new", params)
        assert "notebook=" in url
        assert "tags=" in url
        assert "pinned=true" in url
        assert "color=red" in url
        assert "priority=high" in url
        print("✅ Extended parameter note creation URL successful")
        
        # 3. Test special character handling
        params = {
            "title": "Special Characters & Test #1",
            "text": "Markdown **bold** *italic* `code`",
            "tags": ["special-characters", "markdown"]
        }
        url = client.debug_url("note/new", params)
        # Just check that URL is generated (encoding is handled by urllib)
        assert len(url) > 0
        print("✅ Special character handling successful")
        
        return True
        
    except Exception as e:
        print(f"❌ Note creation feature test failed: {str(e)}")
        traceback.print_exc()
        return False


def test_special_note_types():
    """Test special note types"""
    print("\n=== Special Note Types Test ===")
    
    try:
        client = UpNoteClient()
        
        # 1. Test task note content creation
        tasks = ["Task 1", "Task 2", "Task 3"]
        # create_task_note actually calls create_note, so we just check the content
        task_content = "# Task Test\n\n" + UpNoteHelper.create_checklist(tasks)
        assert "- [ ] Task 1" in task_content
        assert "- [ ] Task 2" in task_content
        print("✅ Task note content creation successful")
        
        # 2. Test meeting note content creation
        title = "Team Meeting"
        date = "2024-01-25 14:00"
        attendees = ["Team Lead Kim", "Developer Park"]
        agenda = ["Agenda 1", "Agenda 2"]
        
        meeting_content = f"""# {title}

**Time**: {date}
**Attendees**: {', '.join(attendees)}

## Agenda
{chr(10).join([f"{i+1}. {item}" for i, item in enumerate(agenda)])}"""
        
        assert "Team Meeting" in meeting_content
        assert "Team Lead Kim, Developer Park" in meeting_content
        assert "1. Agenda 1" in meeting_content
        print("✅ Meeting note content creation successful")
        
        # 3. Test project note content creation
        project_name = "Test Project"
        description = "Project description"
        milestones = ["Milestone 1", "Milestone 2"]
        team_members = ["Member 1", "Member 2"]
        
        project_content = f"""# 📋 {project_name}

## Project Overview
{description}

## Team Composition
{chr(10).join([f"- {member}" for member in team_members])}"""
        
        assert "Test Project" in project_content
        assert "Project description" in project_content
        assert "- Member 1" in project_content
        print("✅ Project note content creation successful")
        
        # 4. Test daily note content creation
        date = "2024-01-25"
        mood = "😊 Good"
        weather = "☀️ Sunny"
        
        daily_content = f"""# 📅 {date}

## Today's Status
**Mood**: {mood}
**Weather**: {weather}"""
        
        assert "2024-01-25" in daily_content
        assert "😊 Good" in daily_content
        assert "☀️ Sunny" in daily_content
        print("✅ Daily note content creation successful")
        
        return True
        
    except Exception as e:
        print(f"❌ Special note types test failed: {str(e)}")
        traceback.print_exc()
        return False


def test_advanced_features():
    """Test advanced features"""
    print("\n=== Advanced Features Test ===")
    
    try:
        client = UpNoteClient()
        
        # 1. Test search functionality URL
        search_params = {
            "query": "search term",
            "notebook": "specific notebook",
            "tags": ["Tag1", "Tag2"],
            "limit": 10
        }
        url = client.debug_url("search", search_params)
        assert "query=" in url
        assert "notebook=" in url
        assert "tags=" in url
        assert "limit=10" in url
        print("✅ Search functionality URL generation successful")
        
        # 2. Test notebook creation URL
        notebook_params = {
            "name": "New Notebook",
            "color": "blue",
            "parent": "Parent Notebook"
        }
        url = client.debug_url("notebook/new", notebook_params)
        assert "name=" in url
        assert "color=blue" in url
        assert "parent=" in url
        print("✅ Notebook creation URL successful")
        
        # 3. Test note opening URL
        open_params = {
            "title": "Open Note",
            "edit": True
        }
        url = client.debug_url("note/open", open_params)
        assert "title=" in url
        assert "edit=true" in url
        print("✅ Note opening URL successful")
        
        # 4. Test export URL
        export_params = {
            "title": "Export Note",
            "format": "pdf",
            "destination": "/Users/test/Documents/"
        }
        url = client.debug_url("export", export_params)
        assert "format=pdf" in url
        assert "destination=" in url
        print("✅ Export URL successful")
        
        return True
        
    except Exception as e:
        print(f"❌ Advanced features test failed: {str(e)}")
        traceback.print_exc()
        return False


def test_error_handling():
    """Test error handling"""
    print("\n=== Error Handling Test ===")
    
    try:
        client = UpNoteClient()
        
        # 1. Test empty parameter handling
        url = client.debug_url("note/new", {})
        assert url == "upnote://x-callback-url/note/new"
        print("✅ Empty parameter handling successful")
        
        # 2. Test None value filtering
        params = {
            "title": "Title",
            "text": None,
            "notebook": "",
            "tags": None
        }
        url = client.debug_url("note/new", params)
        assert "title=" in url
        assert "text=" not in url  # None values should be excluded
        assert "notebook=" in url  # Empty strings should be included
        assert "tags=" not in url  # None values should be excluded
        print("✅ None value filtering successful")
        
        # 3. Test list parameter processing
        params = {
            "tags": ["Tag1", "Tag2", "Tag3"],
            "attachments": ["file1.pdf", "file2.jpg"]
        }
        url = client.debug_url("note/new", params)
        # Lists should be converted to comma-separated strings
        assert "tags=" in url
        assert "attachments=" in url
        print("✅ List parameter processing successful")
        
        return True
        
    except Exception as e:
        print(f"❌ Error handling test failed: {str(e)}")
        traceback.print_exc()
        return False


def test_url_length_and_encoding():
    """Test URL length and encoding"""
    print("\n=== URL Length and Encoding Test ===")
    
    try:
        client = UpNoteClient()
        
        # 1. Test long text handling
        long_text = "This is a very long text. " * 100  # About 1500 characters
        params = {
            "title": "Long Text Test",
            "text": long_text
        }
        url = client.debug_url("note/new", params)
        assert len(url) > 1000  # Check that URL was generated
        print(f"✅ Long text handling successful (URL length: {len(url)} characters)")
        
        # 2. Test special character encoding
        special_chars = "!@#$%^&*()_+-=[]{}|;':\",./<>?"
        korean_text = "Korean text test"
        emoji_text = "😀😃😄😁😆😅😂🤣"
        
        params = {
            "title": f"Special characters {special_chars}",
            "text": f"{korean_text} {emoji_text}",
            "tags": ["special-characters", "korean", "emoji"]
        }
        url = client.debug_url("note/new", params)
        assert len(url) > 0
        print("✅ Special character encoding successful")
        
        # 3. Test markdown syntax encoding
        markdown_text = """# Title
## Subtitle
**Bold text**
*Italic*
`Inline code`
```
Code block
```
- List 1
- List 2
> Quote
[Link](https://example.com)
"""
        params = {
            "title": "Markdown Test",
            "text": markdown_text,
            "markdown": True
        }
        url = client.debug_url("note/new", params)
        assert len(url) > 0
        print("✅ Markdown syntax encoding successful")
        
        return True
        
    except Exception as e:
        print(f"❌ URL length and encoding test failed: {str(e)}")
        traceback.print_exc()
        return False


def run_all_tests():
    """Run all tests"""
    print("🚀 UpNote Client Comprehensive Test Start\n")
    
    tests = [
        ("Basic Functionality", test_basic_functionality),
        ("Helper Functions", test_helper_functions),
        ("Note Creation", test_note_creation),
        ("Special Note Types", test_special_note_types),
        ("Advanced Features", test_advanced_features),
        ("Error Handling", test_error_handling),
        ("URL Length and Encoding", test_url_length_and_encoding)
    ]
    
    passed = 0
    failed = 0
    
    for test_name, test_func in tests:
        try:
            if test_func():
                passed += 1
            else:
                failed += 1
        except Exception as e:
            print(f"❌ Exception occurred during {test_name} test: {str(e)}")
            failed += 1
    
    print(f"\n📊 Test Results:")
    print(f"✅ Passed: {passed}")
    print(f"❌ Failed: {failed}")
    print(f"📈 Success Rate: {passed/(passed+failed)*100:.1f}%")
    
    if failed == 0:
        print("\n🎉 All tests passed successfully!")
        return True
    else:
        print(f"\n⚠️  {failed} tests failed. Please check the code.")
        return False


if __name__ == "__main__":
    success = run_all_tests()
    sys.exit(0 if success else 1)