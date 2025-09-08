"""
Final Test Summary and Validation
Verify that all example files work correctly
"""

import subprocess
import sys
from pathlib import Path


def run_test_file(filename: str) -> tuple[bool, str]:
    """Run test file"""
    try:
        result = subprocess.run(
            [sys.executable, filename],
            capture_output=True,
            text=True,
            timeout=30
        )
        return result.returncode == 0, result.stdout + result.stderr
    except subprocess.TimeoutExpired:
        return False, "Test timeout"
    except Exception as e:
        return False, f"Execution error: {str(e)}"


def main():
    """Run all test files"""
    print("🔍 UpNote Client Final Validation Start\n")
    
    test_files = [
        ("Comprehensive Feature Test", "tests/test_all_features.py"),
        ("Basic Usage Example", "examples/example_usage.py"),
        ("Markdown Test", "tests/test_markdown.py"),
        ("Advanced Feature Example", "examples/advanced_example.py"),
        ("Comprehensive Feature Example", "examples/comprehensive_example.py")
    ]
    
    results = []
    
    for test_name, filename in test_files:
        if not Path(filename).exists():
            print(f"❌ {test_name}: File not found ({filename})")
            results.append(False)
            continue
            
        print(f"🧪 Running {test_name}...")
        success, output = run_test_file(filename)
        
        if success:
            print(f"✅ {test_name}: Success")
            results.append(True)
        else:
            print(f"❌ {test_name}: Failed")
            print(f"   Error: {output[:200]}...")
            results.append(False)
    
    # Summary of results
    passed = sum(results)
    total = len(results)
    success_rate = (passed / total) * 100
    
    print(f"\n📊 Final Validation Results:")
    print(f"✅ Passed: {passed}/{total}")
    print(f"❌ Failed: {total - passed}/{total}")
    print(f"📈 Success Rate: {success_rate:.1f}%")
    
    if success_rate == 100:
        print("\n🎉 All examples work perfectly!")
        print("\n📋 Provided Features:")
        print("   • Basic note creation (25+ parameter support)")
        print("   • Markdown-optimized notes")
        print("   • Special note types (tasks, meeting notes, project notes, diary)")
        print("   • Advanced search and filtering")
        print("   • Notebook management")
        print("   • File import/export")
        print("   • Helper functions (checklists, tables, formatting)")
        print("   • Cross-platform support (macOS, Windows, Linux)")
        print("   • Complete URL encoding and error handling")
        
        print("\n🚀 Ready for use!")
        return True
    else:
        print(f"\n⚠️ Issues found in {total - passed} examples.")
        return False


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)