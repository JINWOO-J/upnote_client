"""
UpNote URL Scheme Client
Python class for creating and managing notes using UpNote's x-callback-url
"""

import subprocess
import urllib.parse
from typing import List, Optional, Dict, Any
from datetime import datetime
import platform


class UpNoteClient:
    """Class for creating and managing notes using UpNote URL scheme"""

    def __init__(self):
        """
        Initialize UpNote client
        """
        self.base_scheme = "upnote://x-callback-url"
        self.system = platform.system()

    def _open_url(self, url: str) -> bool:
        """
        Open URL using system-specific method

        Args:
            url (str): URL to open

        Returns:
            bool: Success status
        """
        try:
            if self.system == "Darwin":  # macOS
                subprocess.run(["open", url], check=True)
            elif self.system == "Windows":
                subprocess.run(["start", url], shell=True, check=True)
            elif self.system == "Linux":
                subprocess.run(["xdg-open", url], check=True)
            else:
                raise Exception(f"Unsupported operating system: {self.system}")
            return True
        except subprocess.CalledProcessError as e:
            raise Exception(f"Failed to open URL: {str(e)}")

    def _build_url(self, action: str, params: Dict[str, Any]) -> str:
        """
        Generate UpNote URL scheme URL

        Args:
            action (str): Action (e.g., note/new, note/open)
            params (Dict[str, Any]): URL parameters

        Returns:
            str: Complete URL
        """
        # Remove None values and convert to strings
        clean_params = {}
        for key, value in params.items():
            if value is not None:
                if isinstance(value, list):
                    clean_params[key] = ",".join(str(v) for v in value)
                elif isinstance(value, bool):
                    clean_params[key] = "true" if value else "false"
                else:
                    clean_params[key] = str(value)

        # URL encoding (safely handle markdown characters)
        query_string = urllib.parse.urlencode(clean_params, safe='', quote_via=urllib.parse.quote)
        url = f"{self.base_scheme}/{action}"
        if query_string:
            url += f"?{query_string}"

        return url

    def debug_url(self, action: str, params: Dict[str, Any]) -> str:
        """
        Debugging: Return the URL that would be generated (without actually opening)

        Args:
            action (str): Action
            params (Dict[str, Any]): Parameters

        Returns:
            str: Generated URL
        """
        return self._build_url(action, params)

    def create_note(
        self,
        text: Optional[str] = None,
        title: Optional[str] = None,
        notebook: Optional[str] = None,
        tags: Optional[List[str]] = None,
        markdown: Optional[bool] = True,
        pinned: Optional[bool] = None,
        favorite: Optional[bool] = None,
        starred: Optional[bool] = None,
        color: Optional[str] = None,
        reminder: Optional[str] = None,
        location: Optional[str] = None,
        attachment: Optional[str] = None,
        attachments: Optional[List[str]] = None,
        template: Optional[str] = None,
        folder: Optional[str] = None,
        category: Optional[str] = None,
        priority: Optional[str] = None,
        due_date: Optional[str] = None,
        created_date: Optional[str] = None,
        modified_date: Optional[str] = None,
        author: Optional[str] = None,
        source: Optional[str] = None,
        url: Optional[str] = None,
        encrypted: Optional[bool] = None,
        password: Optional[str] = None,
        readonly: Optional[bool] = None,
        shared: Optional[bool] = None,
        public: Optional[bool] = None,
        format: Optional[str] = None,
        encoding: Optional[str] = None,
        x_success: Optional[str] = None,
        x_error: Optional[str] = None,
        x_cancel: Optional[str] = None
    ) -> bool:
        """
        Create a new note (supports extended UpNote URL scheme parameters)
        """
        params = {}

        # Basic note information
        if text:
            params["text"] = text
        if title:
            params["title"] = title
        if notebook:
            params["notebook"] = notebook
        if folder:
            params["folder"] = folder
        if tags:
            params["tags"] = tags
        if category:
            params["category"] = category

        # Note properties
        if markdown is not None:
            params["markdown"] = markdown
        if pinned is not None:
            params["pinned"] = pinned
        if favorite is not None:
            params["favorite"] = favorite
        if starred is not None:
            params["starred"] = starred
        if color:
            params["color"] = color
        if priority:
            params["priority"] = priority

        # Time-related
        if reminder:
            params["reminder"] = reminder
        if due_date:
            params["due_date"] = due_date
        if created_date:
            params["created_date"] = created_date
        if modified_date:
            params["modified_date"] = modified_date

        # Location and attachments
        if location:
            params["location"] = location
        if attachment:
            params["attachment"] = attachment
        if attachments:
            params["attachments"] = attachments

        # Metadata
        if template:
            params["template"] = template
        if author:
            params["author"] = author
        if source:
            params["source"] = source
        if url:
            params["url"] = url

        # Security and access control
        if encrypted is not None:
            params["encrypted"] = encrypted
        if password:
            params["password"] = password
        if readonly is not None:
            params["readonly"] = readonly
        if shared is not None:
            params["shared"] = shared
        if public is not None:
            params["public"] = public

        # Format and encoding
        if format:
            params["format"] = format
        if encoding:
            params["encoding"] = encoding

        # Callback URLs
        if x_success:
            params["x-success"] = x_success
        if x_error:
            params["x-error"] = x_error
        if x_cancel:
            params["x-cancel"] = x_cancel

        url = self._build_url("note/new", params)
        return self._open_url(url)

    def create_markdown_note(
        self,
        title: str,
        content: str,
        notebook: Optional[str] = None,
        tags: Optional[List[str]] = None,
        add_timestamp: bool = False,
        pinned: Optional[bool] = None,
        favorite: Optional[bool] = None,
        color: Optional[str] = None,
        reminder: Optional[str] = None
    ) -> bool:
        """
        Create a markdown-formatted note (optimized for markdown processing)
        """
        # Format markdown content
        formatted_content = content

        if add_timestamp:
            formatted_content = UpNoteHelper.format_markdown_content(
                content,
                add_timestamp=True
            )

        return self.create_note(
            text=formatted_content,
            title=title,
            notebook=notebook,
            tags=tags,
            markdown=True,
            pinned=pinned,
            favorite=favorite,
            color=color,
            reminder=reminder
        )

    def create_task_note(
        self,
        title: str,
        tasks: List[str],
        notebook: Optional[str] = None,
        due_date: Optional[str] = None,
        priority: str = "medium",
        tags: Optional[List[str]] = None,
        reminder: Optional[str] = None
    ) -> bool:
        """
        Create a note with a task list
        """
        task_content = "# " + title + "\n\n"
        task_content += UpNoteHelper.create_checklist(tasks)

        if due_date:
            task_content += f"\n\n**Due Date**: {due_date}"

        return self.create_note(
            text=task_content,
            title=title,
            notebook=notebook,
            tags=tags or ["todo", "tasks"],
            priority=priority,
            due_date=due_date,
            reminder=reminder,
            markdown=True
        )

    def create_meeting_note(
        self,
        title: str,
        date: str,
        attendees: List[str],
        agenda: List[str],
        notebook: Optional[str] = None,
        location: Optional[str] = None,
        tags: Optional[List[str]] = None
    ) -> bool:
        """
        Create a meeting note
        """
        meeting_content = f"""# {title}

**Time**: {date}
**Attendees**: {', '.join(attendees)}
{f"**Location**: {location}" if location else ""}

## Agenda
{chr(10).join([f"{i+1}. {item}" for i, item in enumerate(agenda)])}

## Discussion Points
[Write discussion points here]

## Decisions Made
- [Decision 1]
- [Decision 2]

## Action Items
{UpNoteHelper.create_checklist([
    "[Task Description] (Person, Due Date)",
    "[Task Description] (Person, Due Date)"
])}

## Next Meeting
**Schedule**: [Next meeting schedule]
"""

        return self.create_note(
            text=meeting_content,
            title=title,
            notebook=notebook or "Meeting Notes",
            tags=tags or ["meeting", "meeting-notes"],
            location=location,
            markdown=True,
            template="meeting"
        )

    def create_project_note(
        self,
        project_name: str,
        description: str,
        milestones: List[str],
        team_members: List[str],
        due_date: Optional[str] = None,
        notebook: Optional[str] = None,
        priority: str = "medium"
    ) -> bool:
        """
        Create a project plan note
        """
        project_content = f"""# 📋 {project_name}

## Project Overview
{description}

## Team Composition
{chr(10).join([f"- {member}" for member in team_members])}

## Key Milestones
{UpNoteHelper.create_checklist(milestones)}

## Progress
- **Start Date**: {datetime.now().strftime('%Y-%m-%d')}
{f"- **Due Date**: {due_date}" if due_date else ""}
- **Current Status**: Planning Phase

## Resources
- Budget: [Budget information]
- Tools: [Tools to be used]
- Reference Materials: [Related document links]

## Risk Factors
- [Risk Factor 1]
- [Risk Factor 2]

## Next Steps
{UpNoteHelper.create_checklist([
    "Requirements analysis",
    "Technology stack decision",
    "Development schedule establishment"
])}
"""

        return self.create_note(
            text=project_content,
            title=f"📋 {project_name}",
            notebook=notebook or "Projects",
            tags=["project", "plan", priority],
            due_date=due_date,
            priority=priority,
            markdown=True,
            template="project"
        )

    def create_daily_note(
        self,
        date: Optional[str] = None,
        mood: Optional[str] = None,
        weather: Optional[str] = None,
        goals: Optional[List[str]] = None,
        reflections: Optional[str] = None,
        notebook: Optional[str] = None
    ) -> bool:
        """
        Create a daily note
        """
        if not date:
            date = datetime.now().strftime('%Y-%m-%d')

        daily_content = f"""# 📅 {date}

## Today's Status
{f"**Mood**: {mood}" if mood else "**Mood**: "}
{f"**Weather**: {weather}" if weather else "**Weather**: "}

## Today's Goals
{UpNoteHelper.create_checklist(goals) if goals else UpNoteHelper.create_checklist([
    "Goal 1",
    "Goal 2",
    "Goal 3"
])}

## Important Things
- [Important Thing 1]
- [Important Thing 2]

## Things Learned
- [Thing Learned 1]
- [Thing Learned 2]

## Things I'm Grateful For
- [Thing I'm Grateful For 1]
- [Thing I'm Grateful For 2]
- [Thing I'm Grateful For 3]

## Daily Reflection
{reflections if reflections else "[Write about your thoughts on today's day]"}

## Tomorrow's Plan
{UpNoteHelper.create_checklist([
    "Tomorrow's Task 1",
    "Tomorrow's Task 2"
])}
"""

        return self.create_note(
            text=daily_content,
            title=f"📅 {date}",
            notebook=notebook or "Diary",
            tags=["diary", "daily", date.replace('-', '')],
            created_date=date,
            markdown=True,
            template="daily"
        )

    def open_note(
        self,
        note_id: Optional[str] = None,
        title: Optional[str] = None,
        edit: Optional[bool] = None,
        x_success: Optional[str] = None,
        x_error: Optional[str] = None,
        x_cancel: Optional[str] = None
    ) -> bool:
        """
        Open an existing note
        """
        params = {}

        if note_id:
            params["id"] = note_id
        if title:
            params["title"] = title
        if edit is not None:
            params["edit"] = edit
        if x_success:
            params["x-success"] = x_success
        if x_error:
            params["x-error"] = x_error
        if x_cancel:
            params["x-cancel"] = x_cancel

        url = self._build_url("note/open", params)
        return self._open_url(url)

    def search_notes(
        self,
        query: str,
        mode: Optional[str] = None,         # 'all_notes', 'notebooks', 'tags', 'filters' 등 (선택)
        notebook_id: Optional[str] = None,  # mode='notebooks'일 때 사용
        tag_id: Optional[str] = None,       # mode='tags'일 때 사용
        filter_id: Optional[str] = None,    # mode='filters'일 때 사용
        space_id: Optional[str] = None,     # 여러 공간을 쓸 때
        x_success: Optional[str] = None,
        x_error: Optional[str] = None,
        x_cancel: Optional[str] = None
    ) -> bool:
        """
        Opens the UpNote search view.
        Official spec: upnote://x-callback-url/view?action=search&query=... (+ optional parameters)
        Reference: https://help.getupnote.com/more/x-callback-url-endpoints (action=search, query)
        """
        if not query or not query.strip():
            raise ValueError("query는 비어 있을 수 없습니다.")

        params = {
            "action": "search",
            "query": query.strip(),
        }
        if mode:
            params["mode"] = mode
        if notebook_id:
            params["notebookId"] = notebook_id
        if tag_id:
            params["tagId"] = tag_id
        if filter_id:
            params["filterId"] = filter_id
        if space_id:
            params["spaceId"] = space_id

        if x_success:
            params["x-success"] = x_success
        if x_error:
            params["x-error"] = x_error
        if x_cancel:
            params["x-cancel"] = x_cancel

        url = self._build_url("view", params)
        return self._open_url(url)


    def create_notebook(
        self,
        title: str,
        color: Optional[str] = None,
        parent: Optional[str] = None,
        x_success: Optional[str] = None,
        x_error: Optional[str] = None,
        x_cancel: Optional[str] = None
    ) -> bool:
        """
        Create a new notebook
        """
        params = {"title": title}

        if color:
            params["color"] = color
        if parent:
            params["parent"] = parent
        if x_success:
            params["x-success"] = x_success
        if x_error:
            params["x-error"] = x_error
        if x_cancel:
            params["x-cancel"] = x_cancel

        url = self._build_url("notebook/new", params)
        return self._open_url(url)

    def open_notebook(
        self,
        name: Optional[str] = None,
        notebook_id: Optional[str] = None,
        x_success: Optional[str] = None,
        x_error: Optional[str] = None,
        x_cancel: Optional[str] = None
    ) -> bool:
        """
        Open a notebook
        """
        params = {}

        if name:
            params["name"] = name
        if notebook_id:
            params["id"] = notebook_id
        if x_success:
            params["x-success"] = x_success
        if x_error:
            params["x-error"] = x_error
        if x_cancel:
            params["x-cancel"] = x_cancel

        url = self._build_url("notebook/open", params)
        return self._open_url(url)

    def open_upnote(
        self,
        x_success: Optional[str] = None,
        x_error: Optional[str] = None
    ) -> bool:
        """
        Open UpNote app
        """
        params = {}

        if x_success:
            params["x-success"] = x_success
        if x_error:
            params["x-error"] = x_error

        url = self._build_url("open", params)
        return self._open_url(url)

    # def quick_note(
    #     self,
    #     text: str,
    #     append: Optional[bool] = None,
    #     prepend: Optional[bool] = None,
    #     x_success: Optional[str] = None,
    #     x_error: Optional[str] = None
    # ) -> bool:
    #     """
    #     Add a quick note (add to existing note or create new note)
    #     """
    #     params = {"text": text}

    #     if append is not None:
    #         params["append"] = append
    #     if prepend is not None:
    #         params["prepend"] = prepend
    #     if x_success:
    #         params["x-success"] = x_success
    #     if x_error:
    #         params["x-error"] = x_error

    #     url = self._build_url("quick", params)
    #     return self._open_url(url)

    def import_note(
        self,
        file_path: str,
        notebook: Optional[str] = None,
        format_type: Optional[str] = None,
        x_success: Optional[str] = None,
        x_error: Optional[str] = None,
        x_cancel: Optional[str] = None
    ) -> bool:
        """
        Import note from file
        """
        params = {"file": file_path}

        if notebook:
            params["notebook"] = notebook
        if format_type:
            params["format"] = format_type
        if x_success:
            params["x-success"] = x_success
        if x_error:
            params["x-error"] = x_error
        if x_cancel:
            params["x-cancel"] = x_cancel

        url = self._build_url("import", params)
        return self._open_url(url)

    def export_note(
        self,
        note_id: Optional[str] = None,
        title: Optional[str] = None,
        format_type: str = "markdown",
        destination: Optional[str] = None,
        x_success: Optional[str] = None,
        x_error: Optional[str] = None,
        x_cancel: Optional[str] = None
    ) -> bool:
        """
        Export note
        """
        params = {"format": format_type}

        if note_id:
            params["id"] = note_id
        if title:
            params["title"] = title
        if destination:
            params["destination"] = destination
        if x_success:
            params["x-success"] = x_success
        if x_error:
            params["x-error"] = x_error
        if x_cancel:
            params["x-cancel"] = x_cancel

        url = self._build_url("export", params)
        return self._open_url(url)


class UpNoteHelper:
    """Helper class for UpNote operations"""

    @staticmethod
    def format_markdown_content(
        content: str,
        add_timestamp: bool = False,
        add_separator: bool = False
    ) -> str:
        """
        Format markdown content
        """
        formatted_content = content

        if add_timestamp:
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            formatted_content = f"*Created: {timestamp}*\n\n{formatted_content}"

        if add_separator:
            formatted_content = f"{formatted_content}\n\n---\n"

        return formatted_content

    @staticmethod
    def create_checklist(items: List[str]) -> str:
        """
        Create checklist
        """
        checklist = "\n".join([f"- [ ] {item}" for item in items])
        return checklist

    @staticmethod
    def create_table(headers: List[str], rows: List[List[str]]) -> str:
        """
        Create markdown table
        """
        if not headers or not rows:
            return ""

        # Create header
        header_row = "| " + " | ".join(headers) + " |"
        separator_row = "| " + " | ".join(["---"] * len(headers)) + " |"

        # Create data rows
        data_rows = []
        for row in rows:
            if len(row) == len(headers):
                data_rows.append("| " + " | ".join(row) + " |")

        return "\n".join([header_row, separator_row] + data_rows)


# Package information
__version__ = "1.0.0"
__author__ = "UpNote Python Client Team"
__email__ = "upnote.python.client@gmail.com"
__description__ = "A Python client for UpNote using URL schemes"

# Make main classes importable at package level
__all__ = ["UpNoteClient", "UpNoteHelper"]
