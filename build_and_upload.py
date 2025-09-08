#!/usr/bin/env python3
"""
Build and Upload Script for PyPI
"""

import os
import sys
import subprocess
import shutil
from pathlib import Path


def run_command(command, description):
    """Execute command"""
    print(f"\n🔄 {description}...")
    try:
        result = subprocess.run(command, shell=True, check=True, capture_output=True, text=True)
        print(f"✅ {description} completed")
        if result.stdout:
            print(f"Output: {result.stdout}")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ {description} failed")
        print(f"Error: {e.stderr}")
        return False


def clean_build_dirs():
    """Clean build directories"""
    dirs_to_clean = ["build", "dist", "*.egg-info"]
    for dir_pattern in dirs_to_clean:
        for path in Path(".").glob(dir_pattern):
            if path.is_dir():
                print(f"🗑️  Deleting directory {path}")
                shutil.rmtree(path)
            elif path.is_file():
                print(f"🗑️  Deleting file {path}")
                path.unlink()


def check_requirements():
    """Check if required tools are installed"""
    required_tools = ["twine", "wheel", "setuptools"]
    missing_tools = []
    
    for tool in required_tools:
        try:
            subprocess.run([sys.executable, "-c", f"import {tool}"], 
                         check=True, capture_output=True)
        except subprocess.CalledProcessError:
            missing_tools.append(tool)
    
    if missing_tools:
        print(f"❌ The following tools are required: {', '.join(missing_tools)}")
        print("Installation command:")
        print(f"pip install {' '.join(missing_tools)}")
        return False
    
    print("✅ All required tools are installed")
    return True


def validate_package():
    """Validate package"""
    print("\n🔍 Validating package...")
    
    # Check required files
    required_files = [
        "setup.py",
        "pyproject.toml", 
        "README.md",
        "LICENSE",
        "upnote_python_client/__init__.py"
    ]
    
    missing_files = []
    for file in required_files:
        if not Path(file).exists():
            missing_files.append(file)
    
    if missing_files:
        print(f"❌ The following files are missing: {', '.join(missing_files)}")
        return False
    
    print("✅ All required files exist")
    return True


def build_package():
    """Build package"""
    if not run_command("python setup.py sdist bdist_wheel", "Building package"):
        return False
    
    # Check built files
    dist_files = list(Path("dist").glob("*"))
    if not dist_files:
        print("❌ No built files found")
        return False
    
    print(f"✅ Built files:")
    for file in dist_files:
        print(f"   📦 {file}")
    
    return True


def check_package():
    """Check package"""
    return run_command("twine check dist/*", "Checking package")


def upload_to_testpypi():
    """Upload to TestPyPI"""
    print("\n🚀 Upload to TestPyPI? (y/N): ", end="")
    if input().lower() != 'y':
        print("Skipping TestPyPI upload")
        return True
    
    return run_command("twine upload --repository testpypi dist/*", "Uploading to TestPyPI")


def upload_to_pypi():
    """Upload to PyPI"""
    print("\n🚀 Upload to actual PyPI? (y/N): ", end="")
    if input().lower() != 'y':
        print("Skipping PyPI upload")
        return True
    
    print("⚠️  Warning: Uploading to actual PyPI cannot be undone!")
    print("Really upload? (yes/N): ", end="")
    if input().lower() != 'yes':
        print("Cancelled PyPI upload")
        return True
    
    return run_command("twine upload dist/*", "Uploading to PyPI")


def main():
    """Main function"""
    print("🏗️  UpNote Python Client PyPI Upload Tool")
    print("=" * 50)
    
    # 1. Check required tools
    if not check_requirements():
        sys.exit(1)
    
    # 2. Validate package
    if not validate_package():
        sys.exit(1)
    
    # 3. Clean existing build files
    clean_build_dirs()
    
    # 4. Build package
    if not build_package():
        sys.exit(1)
    
    # 5. Check package
    if not check_package():
        sys.exit(1)
    
    # # 6. Upload to TestPyPI (optional)
    # if not upload_to_testpypi():
    #     sys.exit(1)
    
    # 7. Upload to PyPI (optional)
    if not upload_to_pypi():
        sys.exit(1)
    
    print("\n🎉 All tasks completed!")
    print("\n📋 Next steps:")
    print("1. Check package on PyPI: https://pypi.org/project/upnote-python-client/")
    print("2. Test installation: pip install upnote-python-client")
    print("3. Update documentation and create GitHub release")


if __name__ == "__main__":
    main()