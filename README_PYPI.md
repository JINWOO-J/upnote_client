# PyPI Upload Guide

## Preparations

### 1. Install Required Tools
```bash
pip install build twine wheel
```

### 2. Prepare PyPI Account
- Create account on [PyPI](https://pypi.org)
- Create account on [TestPyPI](https://test.pypi.org) (for testing)
- Generate API tokens

### 3. Configure Credentials
```bash
# Create ~/.pypirc file
[distutils]
index-servers =
    pypi
    testpypi

[pypi]
username = __token__
password = pypi-your-api-token-here

[testpypi]
repository = https://test.pypi.org/legacy/
username = __token__
password = pypi-your-test-api-token-here
```

## Upload Process

### 1. Automatic Upload (Recommended)
```bash
python build_and_upload.py
```

### 2. Manual Upload

#### 2.1 Clean Build Directory
```bash
rm -rf build/ dist/ *.egg-info/
```

#### 2.2 Build Package
```bash
python -m build
```

#### 2.3 Validate Package
```bash
twine check dist/*
```

#### 2.4 Upload to TestPyPI (Testing)
```bash
twine upload --repository testpypi dist/*
```

#### 2.5 Install Test from TestPyPI
```bash
pip install --index-url https://test.pypi.org/simple/ upnote-python-client
```

#### 2.6 Upload to Actual PyPI
```bash
twine upload dist/*
```

## Post-Upload Checklist

### 1. Check PyPI Page
- https://pypi.org/project/upnote-python-client/

### 2. Installation Test
```bash
pip install upnote-python-client
```

### 3. Functionality Test
```python
from upnote_python_client import UpNoteClient
client = UpNoteClient()
print("Installation successful!")
```

## Version Updates

### 1. Update Version Number
- `version` in `setup.py`
- `version` in `pyproject.toml`
- `__version__` in `upnote_python_client/__init__.py`

### 2. Update CHANGELOG.md
Add changes for the new version

### 3. Create and Push Tags
```bash
git tag v1.0.1
git push origin v1.0.1
```

### 4. Upload New Version
```bash
python build_and_upload.py
```

## Troubleshooting

### 1. Package Name Conflicts
- If the name is already in use on PyPI
- Change `name` in `setup.py` and `pyproject.toml`

### 2. Version Conflicts
- Versions already uploaded cannot be re-uploaded
- Must increment the version number

### 3. Metadata Errors
- Pre-validate with `twine check` command
- Ensure all required fields are filled

### 4. Authentication Errors
- Verify API token is correct
- Check `~/.pypirc` file permissions (600)

## GitHub Actions Automatic Deployment

### 1. Set Secrets
In GitHub repository Settings > Secrets:
- `PYPI_API_TOKEN`: PyPI API token

### 2. Create Release
When you create a new release on GitHub, it will automatically upload to PyPI.

## Notes

1. **Testing Required**: Test on TestPyPI first
2. **Version Management**: Use semantic versioning (major.minor.patch)
3. **Documentation Updates**: Keep README and CHANGELOG up to date
4. **Security**: Never include API tokens in code
5. **Irreversible**: Versions uploaded to PyPI cannot be deleted