#!/usr/bin/env python3
"""
Multiple Files Compression Example

This example demonstrates how to compress multiple files using the SecureZip library,
including various scenarios like file selection, base directory usage, and batch processing.
"""

import shutil
import tempfile
from pathlib import Path

from minizipper import EncryptionAlgorithm, SecureZipper, ZipError


def create_test_file_structure():
    """Create a complex test file structure for demonstration"""
    temp_dir = tempfile.mkdtemp()

    # Create main project directory
    project_dir = Path(temp_dir) / "my_project"
    project_dir.mkdir()

    # Create source code files
    src_dir = project_dir / "src"
    src_dir.mkdir()

    (src_dir / "main.py").write_text("""#!/usr/bin/env python3
def main():
    print("Hello, World!")

if __name__ == "__main__":
    main()
""")

    (src_dir / "utils.py").write_text("""import os
import sys

def get_config():
    return {"debug": True, "port": 8080}

def log_message(message):
    print(f"[INFO] {message}")
""")

    (src_dir / "config.py").write_text("""# Configuration file
DATABASE_URL = "postgresql://localhost/mydb"
API_KEY = "your_api_key_here"
DEBUG = True
""")

    # Create documentation
    docs_dir = project_dir / "docs"
    docs_dir.mkdir()

    (docs_dir / "README.md").write_text("""# My Project

This is a sample project demonstrating multiple file compression.

## Installation

```bash
pip install my-project
```

## Usage

```python
from my_project import main
main()
```
""")

    (docs_dir / "API.md").write_text("""# API Documentation

## Functions

### main()
Main entry point for the application.

### get_config()
Returns configuration dictionary.

### log_message(message)
Logs a message to console.
""")

    # Create test files
    tests_dir = project_dir / "tests"
    tests_dir.mkdir()

    (tests_dir / "test_main.py").write_text("""import pytest
from src.main import main

def test_main():
    # This is a test
    assert True
""")

    (tests_dir / "test_utils.py").write_text("""import pytest
from src.utils import get_config, log_message

def test_get_config():
    config = get_config()
    assert "debug" in config
    assert "port" in config

def test_log_message():
    # Test logging
    log_message("Test message")
    assert True
""")

    # Create data files
    data_dir = project_dir / "data"
    data_dir.mkdir()

    (data_dir / "users.csv").write_text("""id,name,email
1,John Doe,john@example.com
2,Jane Smith,jane@example.com
3,Bob Johnson,bob@example.com
""")

    (data_dir / "config.json").write_text("""{
    "database": {
        "host": "localhost",
        "port": 5432,
        "name": "mydb"
    },
    "api": {
        "version": "v1",
        "timeout": 30
    }
}
""")

    # Create assets
    assets_dir = project_dir / "assets"
    assets_dir.mkdir()

    (assets_dir / "logo.png").write_bytes(b"fake_png_data_here")
    (assets_dir / "icon.ico").write_bytes(b"fake_ico_data_here")

    # Create hidden files
    (project_dir / ".gitignore").write_text("""# Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
build/
develop-eggs/
dist/
downloads/
eggs/
.eggs/
lib/
lib64/
parts/
sdist/
var/
wheels/
*.egg-info/
.installed.cfg
*.egg
""")

    (project_dir / ".env").write_text("""# Environment variables
DATABASE_URL=postgresql://localhost/mydb
API_KEY=your_secret_key_here
DEBUG=True
""")

    return temp_dir, project_dir


def example_1_basic_multiple_files():
    """Example 1: Basic multiple files compression"""
    print("=" * 70)
    print("Example 1: Basic Multiple Files Compression")
    print("=" * 70)

    temp_dir, project_dir = create_test_file_structure()

    try:
        # Create SecureZipper instance using context manager
        with SecureZipper() as zipper:
            # Select specific files to compress
            files_to_compress = [
                project_dir / "src" / "main.py",
                project_dir / "src" / "utils.py",
                project_dir / "docs" / "README.md",
                project_dir / "data" / "users.csv"
            ]

            print("\n📁 Selected files for compression:")
            for file_path in files_to_compress:
                print(f"   📄 {file_path.relative_to(project_dir)}")

            # Create zip with selected files
            output_file = Path(temp_dir) / "selected_files.zip"
            result = zipper.create_zip_from_files(files_to_compress, output_file)

            print(f"\n✅ Created zip file: {result}")
            print(f"📊 Size: {output_file.stat().st_size / 1024:.2f} KB")

            # Test extraction
            if zipper.test_zip_extraction(output_file):
                print("✅ Extraction test: PASSED")
            else:
                print("❌ Extraction test: FAILED")

            # Extract and verify contents
            extract_dir = Path(temp_dir) / "extracted_basic"
            if zipper.extract_zip(output_file, extract_dir):
                print(f"✅ Extracted to: {extract_dir}")

                # List extracted files
                for item in extract_dir.rglob("*"):
                    if item.is_file():
                        print(f"   📄 {item.name}")
            else:
                print("❌ Extraction failed")

        print("✅ Context manager automatically cleaned up")

    except ZipError as e:
        print(f"❌ Error: {e}")
    finally:
        shutil.rmtree(temp_dir, ignore_errors=True)


def example_2_with_base_directory():
    """Example 2: Multiple files with base directory"""
    print("\n" + "=" * 70)
    print("Example 2: Multiple Files with Base Directory")
    print("=" * 70)

    temp_dir, project_dir = create_test_file_structure()

    try:
        zipper = SecureZipper()

        # Select files from different directories
        files_to_compress = [
            project_dir / "src" / "main.py",
            project_dir / "src" / "utils.py",
            project_dir / "tests" / "test_main.py",
            project_dir / "data" / "users.csv",
            project_dir / "docs" / "README.md"
        ]

        print("\n📁 Selected files (with base directory):")
        for file_path in files_to_compress:
            print(f"   📄 {file_path.relative_to(project_dir)}")

        # Create zip with base directory (preserves directory structure)
        output_file = Path(temp_dir) / "with_base_dir.zip"
        result = zipper.create_zip_from_files(
            files_to_compress,
            output_file,
            base_dir=project_dir
        )

        print(f"\n✅ Created zip file: {result}")
        print(f"📊 Size: {output_file.stat().st_size / 1024:.2f} KB")

        # Extract and show preserved structure
        extract_dir = Path(temp_dir) / "extracted_with_base"
        if zipper.extract_zip(output_file, extract_dir):
            print(f"✅ Extracted to: {extract_dir}")

            # Show preserved directory structure
            for item in extract_dir.rglob("*"):
                if item.is_file():
                    rel_path = item.relative_to(extract_dir)
                    print(f"   📄 {rel_path}")
        else:
            print("❌ Extraction failed")

    except ZipError as e:
        print(f"❌ Error: {e}")
    finally:
        shutil.rmtree(temp_dir, ignore_errors=True)


def example_3_file_type_filtering():
    """Example 3: File type filtering and selection"""
    print("\n" + "=" * 70)
    print("Example 3: File Type Filtering and Selection")
    print("=" * 70)

    temp_dir, project_dir = create_test_file_structure()

    try:
        zipper = SecureZipper()

        # Collect all Python files
        python_files = list(project_dir.rglob("*.py"))

        print(f"\n🐍 Found {len(python_files)} Python files:")
        for file_path in python_files:
            print(f"   📄 {file_path.relative_to(project_dir)}")

        # Create zip with only Python files
        output_file = Path(temp_dir) / "python_files.zip"
        result = zipper.create_zip_from_files(python_files, output_file)

        print(f"\n✅ Created Python files zip: {result}")
        print(f"📊 Size: {output_file.stat().st_size / 1024:.2f} KB")

        # Collect all documentation files
        doc_files = []
        for ext in [".md", ".txt"]:
            doc_files.extend(project_dir.rglob(f"*{ext}"))

        print(f"\n📚 Found {len(doc_files)} documentation files:")
        for file_path in doc_files:
            print(f"   📄 {file_path.relative_to(project_dir)}")

        # Create zip with documentation files
        doc_output = Path(temp_dir) / "documentation.zip"
        result = zipper.create_zip_from_files(doc_files, doc_output)

        print(f"\n✅ Created documentation zip: {result}")
        print(f"📊 Size: {doc_output.stat().st_size / 1024:.2f} KB")

        # Collect all data files
        data_files = list(project_dir.rglob("*.csv")) + list(project_dir.rglob("*.json"))

        print(f"\n📊 Found {len(data_files)} data files:")
        for file_path in data_files:
            print(f"   📄 {file_path.relative_to(project_dir)}")

        # Create zip with data files
        data_output = Path(temp_dir) / "data_files.zip"
        result = zipper.create_zip_from_files(data_files, data_output)

        print(f"\n✅ Created data files zip: {result}")
        print(f"📊 Size: {data_output.stat().st_size / 1024:.2f} KB")

    except ZipError as e:
        print(f"❌ Error: {e}")
    finally:
        shutil.rmtree(temp_dir, ignore_errors=True)


def example_4_encrypted_multiple_files():
    """Example 4: Encrypted multiple files compression"""
    print("\n" + "=" * 70)
    print("Example 4: Encrypted Multiple Files Compression")
    print("=" * 70)

    temp_dir, project_dir = create_test_file_structure()

    try:
        # Create SecureZipper instance using context manager
        with SecureZipper() as zipper:
            # Select sensitive files for encryption
            sensitive_files = [
                project_dir / "src" / "config.py",
                project_dir / "data" / "config.json",
                project_dir / ".env"
            ]

            print("\n🔐 Selected sensitive files for encryption:")
            for file_path in sensitive_files:
                print(f"   📄 {file_path.relative_to(project_dir)}")

            # Create encrypted zip with HMAC-SHA256
            zipper.setpassword("secure_password_2024", EncryptionAlgorithm.HMAC_SHA256)

            output_file = Path(temp_dir) / "sensitive_files_encrypted.zip"
            result = zipper.create_zip_from_files(sensitive_files, output_file)

            print(f"\n✅ Created encrypted zip: {result}")
            print(f"📊 Size: {output_file.stat().st_size / 1024:.2f} KB")

            # Test extraction with correct password
            if zipper.test_zip_extraction(output_file):
                print("✅ Extraction test with correct password: PASSED")
            else:
                print("❌ Extraction test with correct password: FAILED")

            # Test extraction with wrong password
            zipper.setpassword("wrong_password")
            if not zipper.test_zip_extraction(output_file):
                print("✅ Extraction test with wrong password: CORRECTLY BLOCKED")
            else:
                print("❌ Extraction test with wrong password: INCORRECTLY ALLOWED")

            # Extract with correct password
            zipper.setpassword("secure_password_2024")
            extract_dir = Path(temp_dir) / "extracted_sensitive"
            if zipper.extract_zip(output_file, extract_dir):
                print(f"✅ Successfully extracted sensitive files to: {extract_dir}")

                # List extracted files
                for item in extract_dir.rglob("*"):
                    if item.is_file():
                        print(f"   📄 {item.name}")
            else:
                print("❌ Extraction failed")

        print("✅ Context manager automatically cleaned up sensitive data")

    except ZipError as e:
        print(f"❌ Error: {e}")
    finally:
        shutil.rmtree(temp_dir, ignore_errors=True)


def example_5_batch_processing():
    """Example 5: Batch processing multiple file sets"""
    print("\n" + "=" * 70)
    print("Example 5: Batch Processing Multiple File Sets")
    print("=" * 70)

    temp_dir, project_dir = create_test_file_structure()

    try:
        zipper = SecureZipper()

        # Define different file sets for batch processing
        file_sets = {
            "source_code": list(project_dir.rglob("*.py")),
            "documentation": list(project_dir.rglob("*.md")) + list(project_dir.rglob("*.txt")),
            "data_files": list(project_dir.rglob("*.csv")) + list(project_dir.rglob("*.json")),
            "assets": list(project_dir.rglob("*.png")) + list(project_dir.rglob("*.ico")),
            "config_files": [project_dir / ".env", project_dir / ".gitignore"]
        }

        print(f"\n🔄 Processing {len(file_sets)} file sets:")

        results = []

        for set_name, files in file_sets.items():
            if not files:
                print(f"   ⚠️  {set_name}: No files found")
                continue

            print(f"\n📦 Processing {set_name} ({len(files)} files):")
            for file_path in files:
                print(f"   📄 {file_path.relative_to(project_dir)}")

            # Create zip for this file set
            output_file = Path(temp_dir) / f"{set_name}.zip"
            result = zipper.create_zip_from_files(files, output_file)

            size_kb = output_file.stat().st_size / 1024
            print(f"   ✅ Created: {result} ({size_kb:.2f} KB)")

            results.append((set_name, output_file, len(files), size_kb))

        # Summary
        print("\n📊 Batch Processing Summary:")
        print(f"{'Set Name':<15} {'Files':<8} {'Size (KB)':<12}")
        print("-" * 40)

        total_files = 0
        total_size = 0

        for set_name, _, file_count, size_kb in results:
            print(f"{set_name:<15} {file_count:<8} {size_kb:<12.2f}")
            total_files += file_count
            total_size += size_kb

        print("-" * 40)
        print(f"{'TOTAL':<15} {total_files:<8} {total_size:<12.2f}")

        # Create a combined zip with all files
        print("\n🔗 Creating combined zip with all files...")
        all_files = []
        for files in file_sets.values():
            all_files.extend(files)

        combined_output = Path(temp_dir) / "all_files_combined.zip"
        result = zipper.create_zip_from_files(all_files, combined_output, base_dir=project_dir)

        combined_size_kb = combined_output.stat().st_size / 1024
        print(f"✅ Combined zip: {result} ({combined_size_kb:.2f} KB)")
        print(f"📊 Compression ratio: {total_size / combined_size_kb:.2f}x")

    except ZipError as e:
        print(f"❌ Error: {e}")
    finally:
        shutil.rmtree(temp_dir, ignore_errors=True)


def example_6_error_handling():
    """Example 6: Error handling in multiple files compression"""
    print("\n" + "=" * 70)
    print("Example 6: Error Handling in Multiple Files Compression")
    print("=" * 70)

    temp_dir, project_dir = create_test_file_structure()

    try:
        zipper = SecureZipper()

        # Test various error conditions
        print("\n🚨 Testing error conditions:")

        # 1. Empty file list
        print("\n1. Empty file list:")
        try:
            zipper.create_zip_from_files([], Path(temp_dir) / "empty.zip")
            print("   ❌ Incorrectly allowed empty file list")
        except ZipError as e:
            print(f"   ✅ Correctly caught empty file list: {e}")

        # 2. Non-existent files in list
        print("\n2. Non-existent files in list:")
        files_with_nonexistent = [
            project_dir / "src" / "main.py",  # Exists
            Path(temp_dir) / "nonexistent.txt",  # Doesn't exist
            project_dir / "docs" / "README.md"  # Exists
        ]

        try:
            zipper.create_zip_from_files(files_with_nonexistent, Path(temp_dir) / "test.zip")
            print("   ❌ Incorrectly allowed non-existent files")
        except ZipError as e:
            print(f"   ✅ Correctly caught non-existent files: {e}")

        # 3. Duplicate files
        print("\n3. Duplicate files:")
        duplicate_files = [
            project_dir / "src" / "main.py",
            project_dir / "src" / "main.py",  # Duplicate
            project_dir / "src" / "utils.py"
        ]

        try:
            output_file = Path(temp_dir) / "duplicates.zip"
            result = zipper.create_zip_from_files(duplicate_files, output_file)
            print(f"   ✅ Handled duplicates gracefully: {result}")
        except ZipError as e:
            print(f"   ❌ Failed to handle duplicates: {e}")

        # 4. Files from different base directories
        print("\n4. Files from different base directories:")
        mixed_files = [
            project_dir / "src" / "main.py",
            Path(temp_dir) / "external_file.txt"  # Different base
        ]

        # Create external file
        (Path(temp_dir) / "external_file.txt").write_text("External file content")

        try:
            output_file = Path(temp_dir) / "mixed_bases.zip"
            result = zipper.create_zip_from_files(mixed_files, output_file)
            print(f"   ✅ Handled mixed base directories: {result}")
        except ZipError as e:
            print(f"   ❌ Failed to handle mixed base directories: {e}")

        # 5. Large number of files
        print("\n5. Large number of files:")
        many_files = []
        for i in range(100):
            file_path = project_dir / f"temp_file_{i:03d}.txt"
            file_path.write_text(f"Content of file {i}")
            many_files.append(file_path)

        try:
            output_file = Path(temp_dir) / "many_files.zip"
            result = zipper.create_zip_from_files(many_files, output_file)
            print(f"   ✅ Handled many files: {result}")
            print(f"   📊 Size: {output_file.stat().st_size / 1024:.2f} KB")
        except ZipError as e:
            print(f"   ❌ Failed to handle many files: {e}")

    except Exception as e:
        print(f"❌ Unexpected error: {e}")
    finally:
        shutil.rmtree(temp_dir, ignore_errors=True)


def main():
    """Main function to run all multiple files examples"""
    print("📦 MiniZipper - Multiple Files Compression Examples")
    print("This script demonstrates various scenarios for compressing multiple files.")

    # Run all examples
    example_1_basic_multiple_files()
    example_2_with_base_directory()
    example_3_file_type_filtering()
    example_4_encrypted_multiple_files()
    example_5_batch_processing()
    example_6_error_handling()

    print("\n" + "=" * 70)
    print("🎉 All multiple files examples completed!")
    print("=" * 70)
    print("\n💡 Key takeaways:")
    print("   • Use base_dir to preserve directory structure")
    print("   • Filter files by type for organized compression")
    print("   • Encrypt sensitive files with strong algorithms")
    print("   • Handle errors gracefully in batch processing")
    print("   • Consider file organization for efficient compression")


if __name__ == "__main__":
    main()
