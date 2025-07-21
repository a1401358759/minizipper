#!/usr/bin/env python3
"""
Basic usage example for MiniZipper

This example demonstrates the basic usage of the SecureZip library,
including creating standard zip files and encrypted zip files.
"""

import shutil
import tempfile
from pathlib import Path

# Import SecureZip
from minizipper import EncryptionAlgorithm, SecureZipper, ZipError


def create_test_files():
    """Create test files for demonstration"""
    # Create temporary directory
    temp_dir = tempfile.mkdtemp()

    # Create test files
    test_dir = Path(temp_dir) / "test_files"
    test_dir.mkdir()

    # Create some text files
    (test_dir / "file1.txt").write_text("This is the content of file 1")
    (test_dir / "file2.txt").write_text("This is the content of file 2")
    (test_dir / "file3.txt").write_text("This is the content of file 3")

    # Create a subdirectory
    sub_dir = test_dir / "subdir"
    sub_dir.mkdir()
    (sub_dir / "subfile.txt").write_text("This is a file in subdirectory")

    # Create a hidden file
    (test_dir / ".hidden.txt").write_text("This is a hidden file")

    return temp_dir, test_dir


def example_1_basic_usage():
    """Example 1: Basic usage - creating standard zip files"""
    print("=" * 60)
    print("Example 1: Basic Usage - Creating Standard Zip Files")
    print("=" * 60)

    temp_dir, test_dir = create_test_files()

    try:
        # Create SecureZipper instance
        zipper = SecureZipper()

        # Example 1.1: Compress a single file
        print("\n1.1 Compressing a single file...")
        single_file = test_dir / "file1.txt"
        output_file = Path(temp_dir) / "single_file.zip"

        result = zipper.create_zip(single_file, output_file)
        print(f"✅ Created: {result}")

        # Example 1.2: Compress an entire directory
        print("\n1.2 Compressing an entire directory...")
        output_dir = Path(temp_dir) / "directory.zip"

        result = zipper.create_zip(test_dir, output_dir)
        print(f"✅ Created: {result}")

        # Example 1.3: Compress directory with hidden files
        print("\n1.3 Compressing directory with hidden files...")
        output_hidden = Path(temp_dir) / "with_hidden.zip"

        result = zipper.create_zip(test_dir, output_hidden, include_hidden=True)
        print(f"✅ Created: {result}")

        # Example 1.4: Compress multiple specific files
        print("\n1.4 Compressing multiple specific files...")
        files = [
            test_dir / "file1.txt",
            test_dir / "file2.txt",
            test_dir / "subdir" / "subfile.txt"
        ]
        output_multiple = Path(temp_dir) / "multiple_files.zip"

        result = zipper.create_zip_from_files(files, output_multiple)
        print(f"✅ Created: {result}")

        # Example 1.5: Test zip extraction
        print("\n1.5 Testing zip extraction...")
        if zipper.test_zip_extraction(output_file):
            print("✅ Single file zip extraction test passed")
        else:
            print("❌ Single file zip extraction test failed")

        if zipper.test_zip_extraction(output_dir):
            print("✅ Directory zip extraction test passed")
        else:
            print("❌ Directory zip extraction test failed")

        # Example 1.6: Extract zip files
        print("\n1.6 Extracting zip files...")
        extract_dir = Path(temp_dir) / "extracted"

        if zipper.extract_zip(output_file, extract_dir):
            print(f"✅ Extracted to: {extract_dir}")
            # List extracted files
            for item in extract_dir.rglob("*"):
                if item.is_file():
                    print(f"   📄 {item.relative_to(extract_dir)}")
        else:
            print("❌ Extraction failed")

    except ZipError as e:
        print(f"❌ Error: {e}")
    finally:
        # Clean up
        shutil.rmtree(temp_dir, ignore_errors=True)


def example_2_encrypted_zip():
    """Example 2: Creating encrypted zip files"""
    print("\n" + "=" * 60)
    print("Example 2: Creating Encrypted Zip Files")
    print("=" * 60)

    temp_dir, test_dir = create_test_files()

    try:
        # Create SecureZipper instance
        zipper = SecureZipper()

        # Example 2.1: Create encrypted zip with default algorithm (XOR)
        print("\n2.1 Creating encrypted zip with default algorithm (XOR)...")
        zipper.setpassword("mypassword123")

        output_encrypted = Path(temp_dir) / "encrypted_xor.zip"
        result = zipper.create_zip(test_dir, output_encrypted)
        print(f"✅ Created: {result}")

        # Example 2.2: Create encrypted zip with HMAC-SHA256 algorithm
        print("\n2.2 Creating encrypted zip with HMAC-SHA256 algorithm...")
        zipper.setpassword("mypassword123", EncryptionAlgorithm.HMAC_SHA256)

        output_hmac = Path(temp_dir) / "encrypted_hmac.zip"
        result = zipper.create_zip(test_dir, output_hmac)
        print(f"✅ Created: {result}")

        # Example 2.3: Create encrypted zip with AES-like algorithm
        print("\n2.3 Creating encrypted zip with AES-like algorithm...")
        zipper.setpassword("mypassword123", EncryptionAlgorithm.AES_LIKE)

        output_aes = Path(temp_dir) / "encrypted_aes.zip"
        result = zipper.create_zip(test_dir, output_aes)
        print(f"✅ Created: {result}")

        # Example 2.4: Test encrypted zip extraction
        print("\n2.4 Testing encrypted zip extraction...")
        zipper.setpassword("mypassword123")

        if zipper.test_zip_extraction(output_encrypted):
            print("✅ XOR encrypted zip extraction test passed")
        else:
            print("❌ XOR encrypted zip extraction test failed")

        if zipper.test_zip_extraction(output_hmac):
            print("✅ HMAC encrypted zip extraction test passed")
        else:
            print("❌ HMAC encrypted zip extraction test failed")

        if zipper.test_zip_extraction(output_aes):
            print("✅ AES-like encrypted zip extraction test passed")
        else:
            print("❌ AES-like encrypted zip extraction test failed")

        # Example 2.5: Extract encrypted zip files
        print("\n2.5 Extracting encrypted zip files...")
        extract_dir = Path(temp_dir) / "extracted_encrypted"

        if zipper.extract_zip(output_encrypted, extract_dir):
            print(f"✅ Extracted XOR encrypted zip to: {extract_dir}")
        else:
            print("❌ XOR encrypted zip extraction failed")

        # Example 2.6: Try to extract without password (should fail)
        print("\n2.6 Trying to extract without password (should fail)...")
        zipper.setpassword(None)  # Disable encryption

        extract_dir_no_pass = Path(temp_dir) / "extracted_no_pass"
        if not zipper.extract_zip(output_encrypted, extract_dir_no_pass):
            print("✅ Correctly failed to extract encrypted zip without password")
        else:
            print("❌ Unexpectedly succeeded in extracting encrypted zip without password")

    except ZipError as e:
        print(f"❌ Error: {e}")
    finally:
        # Clean up
        shutil.rmtree(temp_dir, ignore_errors=True)


def example_3_advanced_features():
    """Example 3: Advanced features"""
    print("\n" + "=" * 60)
    print("Example 3: Advanced Features")
    print("=" * 60)

    temp_dir, test_dir = create_test_files()

    try:
        # Create SecureZipper instance with custom compression level
        zipper = SecureZipper(compression_level=9)  # Maximum compression

        # Example 3.1: Different compression levels
        print("\n3.1 Testing different compression levels...")

        # Level 0 (no compression)
        zipper0 = SecureZipper(compression_level=0)
        output_level0 = Path(temp_dir) / "level0.zip"
        zipper0.create_zip(test_dir, output_level0)

        # Level 9 (maximum compression)
        zipper9 = SecureZipper(compression_level=9)
        output_level9 = Path(temp_dir) / "level9.zip"
        zipper9.create_zip(test_dir, output_level9)

        size_level0 = output_level0.stat().st_size
        size_level9 = output_level9.stat().st_size

        print(f"Level 0 size: {size_level0} bytes")
        print(f"Level 9 size: {size_level9} bytes")
        print(f"Compression ratio: {size_level0 / size_level9:.2f}x")

        # Example 3.2: All encryption algorithms
        print("\n3.2 Testing all encryption algorithms...")

        algorithms = [
            EncryptionAlgorithm.XOR,
            EncryptionAlgorithm.HMAC_SHA256,
            EncryptionAlgorithm.AES_LIKE,
            EncryptionAlgorithm.DOUBLE_XOR,
            EncryptionAlgorithm.CUSTOM_HASH
        ]

        for alg in algorithms:
            zipper.setpassword("testpass", alg)
            output_file = Path(temp_dir) / f"test_{alg.value}.zip"
            result = zipper.create_zip(test_dir, output_file)
            size = output_file.stat().st_size
            print(f"✅ {alg.name}: {size} bytes")

        # Example 3.3: Error handling
        print("\n3.3 Testing error handling...")

        # Try to compress non-existent file
        try:
            zipper.create_zip("/nonexistent/file.txt", "output.zip")
        except ZipError as e:
            print(f"✅ Correctly caught error: {e}")

        # Try to compress empty file list
        try:
            zipper.create_zip_from_files([], "output.zip")
        except ZipError as e:
            print(f"✅ Correctly caught error: {e}")

        # Example 3.4: File size comparison
        print("\n3.4 File size comparison...")

        # Standard zip
        zipper.setpassword(None)
        output_standard = Path(temp_dir) / "standard.zip"
        zipper.create_zip(test_dir, output_standard)
        standard_size = output_standard.stat().st_size

        # Encrypted zip
        zipper.setpassword("testpass")
        output_encrypted = Path(temp_dir) / "encrypted.zip"
        zipper.create_zip(test_dir, output_encrypted)
        encrypted_size = output_encrypted.stat().st_size

        print(f"Standard zip: {standard_size} bytes")
        print(f"Encrypted zip: {encrypted_size} bytes")
        print(f"Encryption overhead: {encrypted_size - standard_size} bytes")

    except ZipError as e:
        print(f"❌ Error: {e}")
    finally:
        # Clean up
        shutil.rmtree(temp_dir, ignore_errors=True)


def example_4_context_manager():
    """Example 4: Using SecureZipper as a context manager"""
    print("\n" + "=" * 60)
    print("Example 4: Using SecureZipper as Context Manager")
    print("=" * 60)

    temp_dir, test_dir = create_test_files()

    try:
        # Example 4.1: Basic context manager usage
        print("\n4.1 Basic context manager usage:")
        with SecureZipper() as zipper:
            zipper.setpassword("context_pass", EncryptionAlgorithm.HMAC_SHA256)
            output_file = Path(temp_dir) / "context_basic.zip"
            result = zipper.create_zip(test_dir, output_file)
            print(f"   ✅ Created: {result}")

        print("   ✅ Context manager automatically cleaned up sensitive data")

        # Example 4.2: Multiple operations in context
        print("\n4.2 Multiple operations in context:")
        with SecureZipper() as zipper:
            zipper.setpassword("multi_pass")

            # Create multiple zips
            for i, file_path in enumerate(test_dir.rglob("*.txt")):
                output_file = Path(temp_dir) / f"context_multi_{i}.zip"
                zipper.create_zip(file_path, output_file)
                print(f"   ✅ Created: {output_file.name}")

        print("   ✅ All operations completed, context cleaned up")

        # Example 4.3: Exception handling in context
        print("\n4.3 Exception handling in context:")
        try:
            with SecureZipper() as zipper:
                zipper.setpassword("error_pass")
                # This will raise an exception
                zipper.create_zip("/nonexistent/file.txt", "output.zip")
        except ZipError as e:
            print(f"   ✅ Exception caught: {e}")

        print("   ✅ Context manager handled exception gracefully")

        # Example 4.4: Nested context managers
        print("\n4.4 Nested context managers:")
        with SecureZipper() as outer_zipper:
            outer_zipper.setpassword("outer_pass")
            print("   ✅ Outer context active")

            with SecureZipper() as inner_zipper:
                inner_zipper.setpassword("inner_pass")
                output_inner = Path(temp_dir) / "nested_inner.zip"
                inner_zipper.create_zip(test_dir, output_inner)
                print("   ✅ Inner context completed")

            print("   ✅ Inner context exited, outer still active")
            output_outer = Path(temp_dir) / "nested_outer.zip"
            outer_zipper.create_zip(test_dir, output_outer)
            print("   ✅ Outer context completed")

        print("   ✅ Both contexts exited properly")

        # Example 4.5: Context manager vs traditional comparison
        print("\n4.5 Context manager vs traditional usage:")

        # Traditional way
        zipper_traditional = SecureZipper()
        zipper_traditional.setpassword("compare_pass")
        output_traditional = Path(temp_dir) / "traditional.zip"
        zipper_traditional.create_zip(test_dir, output_traditional)
        print("   Traditional: Manual instantiation and cleanup")

        # Context manager way
        with SecureZipper() as zipper_context:
            zipper_context.setpassword("compare_pass")
            output_context = Path(temp_dir) / "context.zip"
            zipper_context.create_zip(test_dir, output_context)
            print("   Context Manager: Automatic cleanup")

        print("   ✅ Both methods work identically")

    except Exception as e:
        print(f"❌ Error: {e}")
    finally:
        shutil.rmtree(temp_dir, ignore_errors=True)


def main():
    """Main function to run all examples"""
    print("🔐 MiniZipper Library Examples")
    print("This script demonstrates various features of the SecureZip library.")

    # Run examples
    example_1_basic_usage()
    example_2_encrypted_zip()
    example_3_advanced_features()
    example_4_context_manager()

    print("\n" + "=" * 60)
    print("🎉 All examples completed successfully!")
    print("=" * 60)


if __name__ == "__main__":
    main()
