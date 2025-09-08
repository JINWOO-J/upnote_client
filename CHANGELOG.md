# Changelog

This file documents all notable changes to the UpNote Python Client.

## [1.0.0] - 2025-09-08

### Added
- **Core Features**
  - Note creation using UpNote URL scheme
  - Support for over 25 extended parameters
  - Cross-platform support (macOS, Windows, Linux)

- **Note Creation Features**
  - `create_note()`: Basic note creation
  - `create_markdown_note()`: Markdown-optimized notes
  - `create_task_note()`: Task list notes
  - `create_meeting_note()`: Meeting notes
  - `create_project_note()`: Project plan notes
  - `create_daily_note()`: Daily notes

- **Advanced Features**
  - `search_notes()`: Advanced search and filtering
  - `create_notebook()`: Notebook creation and management
  - `open_notebook()`: Open notebook
  - `import_note()`: Import note from file
  - `export_note()`: Export note
  - `quick_note()`: Quick note addition

- **Helper Functions**
  - `UpNoteHelper.create_checklist()`: Create checklist
  - `UpNoteHelper.create_table()`: Create markdown table
  - `UpNoteHelper.format_markdown_content()`: Format content

- **Extended Parameters**
  - Note properties: `pinned`, `favorite`, `starred`, `color`, `priority`
  - Time management: `reminder`, `due_date`, `created_date`, `modified_date`
  - Metadata: `author`, `source`, `url`, `location`, `template`
  - Security: `encrypted`, `password`, `readonly`, `shared`, `public`
  - Attachments: `attachment`, `attachments`
  - Format: `format`, `encoding`

- **Color Support**
  - red, blue, green, yellow, purple, gray, orange, pink

- **Priority Levels**
  - urgent, high, medium, low

- **Tests and Examples**
  - Comprehensive feature tests (`test_all_features.py`)
  - Markdown tests (`test_markdown.py`)
  - Basic usage examples (`example_usage.py`)
  - Advanced feature examples (`advanced_example.py`)
  - Comprehensive examples (`comprehensive_example.py`)

- **Documentation**
  - Detailed README.md
  - API reference documentation
  - Examples and test guides

### Technical Details
- **URL Encoding**: Safe handling of markdown special characters
- **Error Handling**: Complete exception handling and validation
- **Parameter Validation**: None value filtering and type conversion
- **Cross-Platform**: OS-specific URL opening command support

### Performance
- **URL Length**: Support for content over 12,000 characters
- **Encoding**: Full UTF-8 support
- **Special Characters**: Full support for emojis, Korean characters, and special symbols

### Test Coverage
- **Core Features**: 100% test coverage
- **Helper Functions**: 100% test coverage
- **Error Handling**: 100% test coverage
- **URL Generation**: 100% test coverage

---

## Future Plans

### [1.1.0] - Planned
- **Additional Features**
  - Note template system
  - Batch operation support
  - Configuration file support

- **Improvements**
  - Performance optimization
  - More natural language date format support
  - Additional color options

### [1.2.0] - Planned
- **Integration Features**
  - Compatibility with other note apps
  - Cloud sync support
  - Webhook support

---

## Contribution Guidelines

When adding changes, please follow this format:

### [Version] - Date

#### Added
- New features

#### Changed
- Changes to existing features

#### Fixed
- Bug fixes

#### Removed
- Removed features

#### Security
- Security-related changes