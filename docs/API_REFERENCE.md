# UpNote Client API Reference

## Class Overview

### UpNoteClient
Main class for creating and managing notes using UpNote's x-callback-url.

### UpNoteHelper
Helper class for creating and formatting markdown content.

---

## UpNoteClient Methods

### Basic Note Management

#### `create_note(**kwargs) -> bool`
Creates a new note.

**Parameters:**
- `text` (str, optional): Note content
- `title` (str, optional): Note title
- `notebook` (str, optional): Notebook name
- `tags` (List[str], optional): List of tags
- `markdown` (bool, optional): Whether to render as markdown (default: True)

**Note Properties:**
- `pinned` (bool, optional): Whether to pin the note
- `favorite` (bool, optional): Whether to mark as favorite
- `starred` (bool, optional): Whether to star the note
- `color` (str, optional): Note color (red, blue, green, yellow, purple, gray, orange, pink)
- `priority` (str, optional): Priority (high, medium, low, urgent)

**Time-related:**
- `reminder` (str, optional): Reminder time (ISO 8601 format or natural language)
- `due_date` (str, optional): Due date (ISO 8601 format)
- `created_date` (str, optional): Created date
- `modified_date` (str, optional): Modified date

**Metadata:**
- `author` (str, optional): Author information
- `source` (str, optional): Source information
- `url` (str, optional): Related URL link
- `location` (str, optional): Location information or GPS coordinates
- `template` (str, optional): Template name to use
- `folder` (str, optional): Folder path
- `category` (str, optional): Category classification

**Attachments:**
- `attachment` (str, optional): Single attachment file path
- `attachments` (List[str], optional): Multiple attachment file paths

**Security and Access Control:**
- `encrypted` (bool, optional): Whether to encrypt
- `password` (str, optional): Note password
- `readonly` (bool, optional): Read-only status
- `shared` (bool, optional): Whether to share
- `public` (bool, optional): Whether to make public

**Format and Encoding:**
- `format` (str, optional): File format (markdown, html, txt, rtf)
- `encoding` (str, optional): Text encoding (utf-8, utf-16, etc.)

**Callback URLs:**
- `x_success` (str, optional): Success callback URL
- `x_error` (str, optional): Error callback URL
- `x_cancel` (str, optional): Cancel callback URL

**Return Value:** `bool` - Whether execution was successful

**Example:**
```python
client = UpNoteClient()

# Create basic note
client.create_note(
    title="Meeting Notes",
    text="Summarize today's meeting content.",
    tags=["meeting", "work"]
)

# Create note with advanced settings
client.create_note(
    title="Important Project",
    text="# Project Overview

Important project.",
    notebook="Work",
    priority="high",
    pinned=True,
    color="red",
    due_date="2024-12-31",
    reminder="2024-12-30T09:00:00"
)
```

#### `open_note(**kwargs) -> bool`
Opens an existing note.

**Parameters:**
- `note_id` (str, optional): Note ID to open
- `title` (str, optional): Open note by title search
- `edit` (bool, optional): Whether to open in edit mode
- `x_success` (str, optional): Success callback URL
- `x_error` (str, optional): Error callback URL
- `x_cancel` (str, optional): Cancel callback URL

**Example:**
```python
# Open note by ID
client.open_note(note_id="12345")

# Find note by title and open in edit mode
client.open_note(title="Meeting Notes", edit=True)
```

### Special Note Creation

#### `create_markdown_note(**kwargs) -> bool`
Creates a note optimized for markdown.

**Parameters:**
- `title` (str): Note title
- `content` (str): Markdown content
- `notebook` (str, optional): Notebook name
- `tags` (List[str], optional): List of tags
- `add_timestamp` (bool): Whether to add timestamp
- `pinned` (bool, optional): Whether to pin the note
- `favorite` (bool, optional): Whether to mark as favorite
- `color` (str, optional): Note color
- `reminder` (str, optional): Reminder time

**Example:**
```python
client.create_markdown_note(
    title="Markdown Note",
    content="# Title

**Bold text** and *italic*",
    add_timestamp=True,
    color="blue"
)
```

#### `create_task_note(**kwargs) -> bool`
Creates a note with a task list.

**Parameters:**
- `title` (str): Note title
- `tasks` (List[str]): List of tasks
- `notebook` (str, optional): Notebook name
- `due_date` (str, optional): Due date
- `priority` (str): Priority (default: "medium")
- `tags` (List[str], optional): List of tags
- `reminder` (str, optional): Reminder time

**Example:**
```python
client.create_task_note(
    title="Weekly Tasks",
    tasks=["Write report", "Attend meeting", "Code review"],
    due_date="2024-01-31",
    priority="high"
)
```

#### `create_meeting_note(**kwargs) -> bool`
Creates a meeting note.

**Parameters:**
- `title` (str): Meeting title
- `date` (str): Meeting time
- `attendees` (List[str]): List of attendees
- `agenda` (List[str]): List of agenda items
- `notebook` (str, optional): Notebook name
- `location` (str, optional): Meeting location
- `tags` (List[str], optional): List of tags

**Example:**
```python
client.create_meeting_note(
    title="Team Meeting",
    date="2024-01-25 14:00",
    attendees=["Team Lead Kim", "Developer Park", "Designer Lee"],
    agenda=["Project progress", "Next sprint plan"],
    location="Conference Room A"
)
```

#### `create_project_note(**kwargs) -> bool`
Creates a project plan note.

**Parameters:**
- `project_name` (str): Project name
- `description` (str): Project description
- `milestones` (List[str]): List of milestones
- `team_members` (List[str]): List of team members
- `due_date` (str, optional): Project due date
- `notebook` (str, optional): Notebook name
- `priority` (str): Priority (default: "medium")

**Example:**
```python
client.create_project_note(
    project_name="Website Redesign",
    description="Improve UI/UX of existing website",
    milestones=["Planning", "Design", "Development", "Testing"],
    team_members=["Planner", "Designer", "Developer"],
    due_date="2024-06-30"
)
```

#### `create_daily_note(**kwargs) -> bool`
Creates a daily note.

**Parameters:**
- `date` (str, optional): Date (default: today)
- `mood` (str, optional): Mood
- `weather` (str, optional): Weather
- `goals` (List[str], optional): Today's goals
- `reflections` (str, optional): Daily reflections
- `notebook` (str, optional): Notebook name

**Example:**
```python
client.create_daily_note(
    mood="😊 Good",
    weather="☀️ Sunny",
    goals=["Exercise", "Reading", "Project progress"],
    reflections="Today was a productive day."
)
```

### Search and Navigation

#### `search_notes(**kwargs) -> bool`
Searches for notes.

**Parameters:**
- `query` (str): Search term
- `notebook` (str, optional): Search only in specific notebook
- `tags` (List[str], optional): Filter by specific tags
- `limit` (int, optional): Limit search results
- `x_success` (str, optional): Success callback URL
- `x_error` (str, optional): Error callback URL
- `x_cancel` (str, optional): Cancel callback URL

**Example:**
```python
# Basic search
client.search_notes("project")

# Advanced search
client.search_notes(
    query="meeting",
    notebook="work",
    tags=["important", "in-progress"],
    limit=10
)
```

### Notebook Management

#### `create_notebook(**kwargs) -> bool`
Creates a new notebook.

**Parameters:**
- `name` (str): Notebook name
- `color` (str, optional): Notebook color
- `parent` (str, optional): Parent notebook name (for creating sub-notebooks)
- `x_success` (str, optional): Success callback URL
- `x_error` (str, optional): Error callback URL
- `x_cancel` (str, optional): Cancel callback URL

**Example:**
```python
# Create basic notebook
client.create_notebook("New Project")

# Create notebook with color
client.create_notebook("Data Analysis", color="purple")

# Create sub-notebook
client.create_notebook("Monthly Report", parent="Data Analysis")
```

#### `open_notebook(**kwargs) -> bool`
Opens a notebook.

**Parameters:**
- `name` (str, optional): Notebook name
- `notebook_id` (str, optional): Notebook ID
- `x_success` (str, optional): Success callback URL
- `x_error` (str, optional): Error callback URL
- `x_cancel` (str, optional): Cancel callback URL

### File Operations

#### `import_note(**kwargs) -> bool`
Imports a note from a file.

**Parameters:**
- `file_path` (str): Path to file to import
- `notebook` (str, optional): Target notebook
- `format_type` (str, optional): File format (markdown, txt, html, etc.)
- `x_success` (str, optional): Success callback URL
- `x_error` (str, optional): Error callback URL
- `x_cancel` (str, optional): Cancel callback URL

#### `export_note(**kwargs) -> bool`
Exports a note.

**Parameters:**
- `note_id` (str, optional): Note ID to export
- `title` (str, optional): Search by note title
- `format_type` (str): Export format (default: "markdown")
- `destination` (str, optional): Save path
- `x_success` (str, optional): Success callback URL
- `x_error` (str, optional): Error callback URL
- `x_cancel` (str, optional): Cancel callback URL

### Other Features

#### `quick_note(**kwargs) -> bool`
Adds a quick note.

**Parameters:**
- `text` (str): Text to add
- `append` (bool, optional): Append to end of existing note
- `prepend` (bool, optional): Prepend to beginning of existing note
- `x_success` (str, optional): Success callback URL
- `x_error` (str, optional): Error callback URL

#### `open_upnote(**kwargs) -> bool`
Opens the UpNote app.

**Parameters:**
- `x_success` (str, optional): Success callback URL
- `x_error` (str, optional): Error callback URL

#### `debug_url(action: str, params: Dict[str, Any]) -> str`
Returns the URL that would be generated for debugging (without actually opening).

**Parameters:**
- `action` (str): Action (e.g., "note/new", "search")
- `params` (Dict[str, Any]): URL parameters

**Return Value:** `str` - Generated URL

---

## UpNoteHelper Methods

### `format_markdown_content(content: str, add_timestamp: bool = False, add_separator: bool = False) -> str`
Formats markdown content.

**Parameters:**
- `content` (str): Original content
- `add_timestamp` (bool): Whether to add timestamp
- `add_separator` (bool): Whether to add separator

**Return Value:** `str` - Formatted content

### `create_checklist(items: List[str]) -> str`
Creates a checklist.

**Parameters:**
- `items` (List[str]): Checklist items

**Return Value:** `str` - Markdown checklist

**Example:**
```python
checklist = UpNoteHelper.create_checklist([
    "Task 1",
    "Task 2", 
    "Task 3"
])
# Result: "- [ ] Task 1
- [ ] Task 2
- [ ] Task 3"
```

### `create_table(headers: List[str], rows: List[List[str]]) -> str`
Creates a markdown table.

**Parameters:**
- `headers` (List[str]): Table headers
- `rows` (List[List[str]]): Table row data

**Return Value:** `str` - Markdown table

**Example:**
```python
table = UpNoteHelper.create_table(
    headers=["Name", "Age", "Job"],
    rows=[
        ["Kim Chul-soo", "30", "Developer"],
        ["Lee Young-hee", "25", "Designer"]
    ]
)
```

---

## Supported Colors

- `red`: Red (urgent, important)
- `blue`: Blue (information, planning)
- `green`: Green (completed, success)
- `yellow`: Yellow (caution, waiting)
- `purple`: Purple (creative, ideas)
- `gray`: Gray (archived, reference)
- `orange`: Orange (warning, alert)
- `pink`: Pink (personal, hobbies)

## Priority Levels

- `urgent`: Urgent
- `high`: High
- `medium`: Medium (default)
- `low`: Low

## Date Formats

### ISO 8601 Format
- `2024-01-25T14:30:00` (date and time)
- `2024-01-25` (date only)

### Natural Language Format (supported in reminder)
- `"tomorrow 2pm"`
- `"next friday"`
- `"in 1 hour"`
- `"in 30 minutes"`