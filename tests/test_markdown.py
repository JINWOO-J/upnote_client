"""
Markdown Test Script
Test if markdown renders properly in UpNote
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


def test_markdown_features():
    """Test various markdown features"""
    client = UpNoteClient()
    
    # 1. Basic markdown test
    print("1. Basic markdown test...")
    basic_markdown = """# Heading 1
## Heading 2
### Heading 3

**Bold text** and *italic text*

`Inline code`

```python
# Code block
def hello():
    print("Hello UpNote!")
```

> Quote

- List item 1
- List item 2
  - Sub-item 1
  - Sub-item 2

1. Numbered list 1
2. Numbered list 2

[Link](https://example.com)

---

Content above and below separator
"""
    
    success = client.create_markdown_note(
        title="Markdown Basic Features Test",
        content=basic_markdown,
        tags=["test", "markdown"],
        add_timestamp=True
    )
    print(f"Basic markdown note creation: {'successful' if success else 'failed'}")
    
    # 2. Checklist test
    print("\n2. Checklist test...")
    checklist_content = """# Project Task List

## Development Tasks
{checklist}

## Completed Tasks
- [x] Project initial setup
- [x] Basic structure design
- [x] Development environment setup
""".format(
        checklist=UpNoteHelper.create_checklist([
            "API design and implementation",
            "Frontend UI development",
            "Database schema design",
            "Test code writing",
            "Documentation"
        ])
    )
    
    success = client.create_markdown_note(
        title="Project Checklist",
        content=checklist_content,
        notebook="Project Management",
        tags=["todo", "checklist", "project"]
    )
    print(f"Checklist note creation: {'successful' if success else 'failed'}")
    
    # 3. Table test
    print("\n3. Table test...")
    
    # Project status table
    project_table = UpNoteHelper.create_table(
        headers=["Feature", "Assignee", "Progress", "Due Date", "Status"],
        rows=[
            ["User Authentication", "Kim Dev", "90%", "2024-01-15", "🟡 In Progress"],
            ["Product Management", "Park Coder", "60%", "2024-01-20", "🟡 In Progress"],
            ["Order System", "Lee Pro", "30%", "2024-01-25", "🔴 Delayed"],
            ["Payment Integration", "Choi Dev", "0%", "2024-01-30", "⚪ Pending"]
        ]
    )
    
    # Tech stack table
    tech_table = UpNoteHelper.create_table(
        headers=["Area", "Technology", "Version", "Purpose"],
        rows=[
            ["Frontend", "React", "18.2.0", "UI Framework"],
            ["Backend", "Node.js", "18.17.0", "Server Runtime"],
            ["Database", "PostgreSQL", "15.3", "Main Database"],
            ["Cache", "Redis", "7.0", "Session and Cache"],
            ["Deploy", "Docker", "24.0", "Containerization"]
        ]
    )
    
    table_content = f"""# Project Status Dashboard

## 📊 Development Progress
{project_table}

## 🛠 Tech Stack
{tech_table}

## 📈 Key Metrics
- **Overall Progress**: 45%
- **Completed Features**: 0
- **In Progress Features**: 2
- **Delayed Features**: 1

## 🚨 Notices
> **Order System** is delayed. Resource reallocation may be needed.

## 📅 Next Milestones
- [ ] User authentication completion (1/15)
- [ ] Product management completion (1/20)
- [ ] Order system schedule adjustment
"""
    
    success = client.create_markdown_note(
        title="Project Status Dashboard",
        content=table_content,
        notebook="Project Management",
        tags=["status", "table", "dashboard"]
    )
    print(f"Table note creation: {'successful' if success else 'failed'}")
    
    # 4. Complex markdown test
    print("\n4. Complex markdown test...")
    
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M")
    
    js_code = '''```javascript
// Image lazy loading implementation needed
const LazyImage = (props) => {
  const [loaded, setLoaded] = useState(false);
  
  return (
    <img 
      src={loaded ? props.src : placeholder}
      alt={props.alt}
      onLoad={() => setLoaded(true)}
    />
  );
};
```'''

    sql_code = '''```sql
-- Add indexes for search performance improvement
CREATE INDEX idx_products_category ON products(category_id);
CREATE INDEX idx_orders_user_date ON orders(user_id, created_at);
```'''

    meeting_notes = f"""# 📋 Weekly Team Meeting Notes

**Time**: {current_time}
**Attendees**: Team Lead Kim, Developer Park, Designer Lee, Planner Choi

## 🎯 Key Agenda

### 1. Sprint Review
- ✅ **Completed Tasks**
  - User login/registration feature
  - Basic UI component library
  - API documentation draft

- ⏳ **In Progress Tasks**
  - Product catalog page
  - Shopping cart feature
  - Payment system integration

### 2. Technical Issues

#### Performance Optimization
{js_code}

#### Database Indexing
{sql_code}

### 3. Action Items
{UpNoteHelper.create_checklist([
    "Evaluate image optimization library (Developer Park)",
    "Apply database indexes (Team Lead Kim)",
    "Mobile responsive testing (Designer Lee)",
    "Write user test scenarios (Planner Choi)"
])}

## 📊 Sprint Metrics

{UpNoteHelper.create_table(
    headers=["Metric", "Goal", "Actual", "Achievement"],
    rows=[
        ["Story Points", "40", "35", "87.5%"],
        ["Bug Fixes", "15", "18", "120%"],
        ["Code Coverage", "80%", "75%", "93.8%"],
        ["User Satisfaction", "4.5", "4.2", "93.3%"]
    ]
)}

## 🔮 Next Sprint Plan

### High Priority
1. **Payment System Completion** - Directly affects revenue
2. **Mobile Optimization** - Improves user experience
3. **Performance Tuning** - Reduce loading time

### Medium Priority
- Admin dashboard improvement
- Notification system setup
- Multilingual support preparation

---

> 💡 **Retrospective**: This sprint generally achieved its goals, but we need to focus more on performance issues.

**Next Meeting**: January 22, 2024 (Mon) 2 PM
"""
    
    success = client.create_markdown_note(
        title=f"Weekly Team Meeting - {datetime.now().strftime('%Y-%m-%d')}",
        content=meeting_notes,
        notebook="Meeting Notes",
        tags=["meeting", "team", "sprint", "review"]
    )
    print(f"Complex markdown note creation: {'successful' if success else 'failed'}")


def debug_urls():
    """Check generated URLs"""
    print("\n=== URL Debugging ===")
    client = UpNoteClient()
    
    test_cases = [
        {
            "name": "Basic Text",
            "params": {"text": "Hello World", "title": "Test"}
        },
        {
            "name": "Markdown Headers",
            "params": {"text": "# Title
## Subtitle", "title": "Markdown Test"}
        },
        {
            "name": "Markdown Lists",
            "params": {"text": "- [ ] Task 1
- [x] Completed task", "title": "Checklist"}
        },
        {
            "name": "Code Blocks",
            "params": {"text": "```python
print('hello')
```", "title": "Code"}
        }
    ]
    
    for case in test_cases:
        url = client.debug_url("note/new", case["params"])
        print(f"\n{case['name']}:")
        print(f"URL: {url}")


if __name__ == "__main__":
    test_markdown_features()
    debug_urls()