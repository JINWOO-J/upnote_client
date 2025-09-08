# UpNote Client Tests

This directory contains test files that verify the functionality of the UpNote client.

## Test Files

### 🧪 test_all_features.py
Main test file that comprehensively tests all features.

**Test Items:**
- Basic features (client initialization, URL generation, parameter processing)
- Helper functions (checklists, tables, markdown formatting)
- Note creation features (basic, extended parameters, special characters)
- Special note types (tasks, meeting notes, project notes, diary)
- Advanced features (search, notebook management, export)
- Error handling (empty parameters, None values, list processing)
- URL length and encoding (long text, special characters, markdown)

**How to Run:**
```bash
cd tests
python test_all_features.py
```

### 📝 test_markdown.py
Focuses on testing markdown features.

**Test Items:**
- Basic markdown syntax (headers, bold, italic, code)
- Checklist creation and rendering
- Table creation and formatting
- Complex markdown documents (code blocks, quotes, links)
- URL encoding and special character handling

**How to Run:**
```bash
cd tests
python test_markdown.py
```

### 📊 final_test_summary.py
Performs final validation by running all examples and tests.

**Features:**
- Automatically runs all example files
- Collects success/failure results
- Calculates overall success rate
- Outputs feature summary

**How to Run:**
```bash
cd tests
python final_test_summary.py
```

## Test Execution Guide

### Run All Tests
```bash
# Run main test
python tests/test_all_features.py

# Run markdown test  
python tests/test_markdown.py

# Run final validation
python tests/final_test_summary.py
```

### Individual Feature Tests
Each test file can be run independently, which is useful when you want to test only specific features.

## Interpreting Test Results

### Success Cases
```
✅ Basic feature test successful
✅ Helper function test successful
📈 Success rate: 100.0%
🎉 All tests passed successfully!
```

### Failure Cases
```
❌ Basic feature test failed: Error message
📈 Success rate: 85.7%
⚠️ 1 test failed.
```

## Notes

- **URL Generation Tests**: Only test URL generation without opening the actual UpNote app.
- **Cross-Platform**: Can run on macOS, Windows, and Linux.
- **Dependencies**: Uses only Python standard libraries, no external libraries required.

## Adding Tests

If you've added new features, please add corresponding tests:

1. Add new test function to `test_all_features.py`
2. Add test function to the test list in `run_all_tests()`
3. Write assert statements comparing expected and actual results

## Debugging

If tests fail, check the following:

1. **Module import**: Verify that `upnote_client.py` is in the correct location
2. **Python version**: Use Python 3.7 or higher
3. **File permissions**: Verify that test files are executable
4. **Error messages**: Check detailed error messages to identify the problem