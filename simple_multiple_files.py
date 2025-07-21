#!/usr/bin/env python3
"""
Simple Multiple Files Example

A simple example showing how to compress multiple files using SecureZip.
"""

import shutil
import tempfile
from pathlib import Path

from minizipper import SecureZipper, ZipError


def main():
    """Main function"""
    # Create temporary directory for testing
    temp_dir = tempfile.mkdtemp()

    try:
        # Create test files
        test_dir = Path(temp_dir) / "test_files"
        test_dir.mkdir()

        # Create some text files
        (test_dir / "file1.txt").write_text("This is file 1 content")
        (test_dir / "file2.txt").write_text("This is file 2 content")
        (test_dir / "file3.txt").write_text("This is file 3 content")

        # Create a subdirectory with more files
        sub_dir = test_dir / "subdir"
        sub_dir.mkdir()
        (sub_dir / "subfile1.txt").write_text("This is subfile 1")
        (sub_dir / "subfile2.txt").write_text("This is subfile 2")

        print("📁 Created test files:")
        for file_path in test_dir.rglob("*"):
            if file_path.is_file():
                print(f"   📄 {file_path.relative_to(test_dir)}")

        # Create SecureZipper instance
        zipper = SecureZipper()

        # Method 1: Compress entire directory
        print("\n📦 Method 1: Compress entire directory")
        output_file1 = Path(temp_dir) / "method1_directory.zip"
        result1 = zipper.create_zip(test_dir, output_file1)
        print(f"✅ Created: {result1}")

        # Method 2: Compress specific files
        print("\n📦 Method 2: Compress specific files")
        specific_files = [
            test_dir / "file1.txt",
            test_dir / "file2.txt",
            sub_dir / "subfile1.txt"
        ]

        output_file2 = Path(temp_dir) / "method2_specific.zip"
        result2 = zipper.create_zip_from_files(specific_files, output_file2)
        print(f"✅ Created: {result2}")

        # Method 3: Compress with base directory
        print("\n📦 Method 3: Compress with base directory")
        output_file3 = Path(temp_dir) / "method3_base_dir.zip"
        result3 = zipper.create_zip_from_files(specific_files, output_file3, base_dir=test_dir)
        print(f"✅ Created: {result3}")

        # Method 4: Using context manager (recommended)
        print("\n📦 Method 4: Using context manager (recommended)")
        with SecureZipper() as zipper_context:
            output_file4 = Path(temp_dir) / "method4_context.zip"
            result4 = zipper_context.create_zip(test_dir, output_file4)
            print(f"✅ Created: {result4}")
        print("✅ Context manager automatically cleaned up")

        # Test extraction
        print("\n🔍 Testing extraction:")

        # Test method 1
        if zipper.test_zip_extraction(output_file1):
            print("✅ Method 1 extraction test: PASSED")
        else:
            print("❌ Method 1 extraction test: FAILED")

        # Test method 2
        if zipper.test_zip_extraction(output_file2):
            print("✅ Method 2 extraction test: PASSED")
        else:
            print("❌ Method 2 extraction test: FAILED")

        # Test method 3
        if zipper.test_zip_extraction(output_file3):
            print("✅ Method 3 extraction test: PASSED")
        else:
            print("❌ Method 3 extraction test: FAILED")

        # Extract and show contents
        print("\n📂 Extracting method 3 zip:")
        extract_dir = Path(temp_dir) / "extracted"
        if zipper.extract_zip(output_file3, extract_dir):
            print(f"✅ Extracted to: {extract_dir}")

            # List extracted files
            for item in extract_dir.rglob("*"):
                if item.is_file():
                    print(f"   📄 {item.relative_to(extract_dir)}")
        else:
            print("❌ Extraction failed")

        # Show file sizes
        print("\n📊 File size comparison:")
        for i, output_file in enumerate([output_file1, output_file2, output_file3], 1):
            size_kb = output_file.stat().st_size / 1024
            print(f"   Method {i}: {size_kb:.2f} KB")

    except ZipError as e:
        print(f"❌ Error: {e}")
    finally:
        # Clean up
        shutil.rmtree(temp_dir, ignore_errors=True)


if __name__ == "__main__":
    main()
