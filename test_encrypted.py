#!/usr/bin/env python3
"""
Test encrypted zip functionality

This script tests the encrypted zip functionality of the SecureZip library.
"""

import shutil
import tempfile
from pathlib import Path

from minizipper import EncryptionAlgorithm, SecureZipper


def test_encryption_algorithms():
    """Test all encryption algorithms"""
    print("Testing all encryption algorithms...")

    temp_dir = tempfile.mkdtemp()

    try:
        # Create test file
        test_file = Path(temp_dir) / "test.txt"
        test_file.write_text("This is a test file for encryption.")

        # Test each algorithm using context manager
        algorithms = [
            EncryptionAlgorithm.XOR,
            EncryptionAlgorithm.HMAC_SHA256,
            EncryptionAlgorithm.AES_LIKE,
            EncryptionAlgorithm.DOUBLE_XOR,
            EncryptionAlgorithm.CUSTOM_HASH
        ]

        for alg in algorithms:
            print(f"\nTesting {alg.name}...")

            # Use context manager for automatic cleanup
            with SecureZipper() as zipper:
                # Set password and algorithm
                zipper.setpassword("testpass", alg)

                # Create encrypted zip
                output_file = Path(temp_dir) / f"test_{alg.value}.zip"
                result = zipper.create_zip(test_file, output_file)

                print(f"  Created: {result}")

                # Test extraction
                if zipper.test_zip_extraction(output_file):
                    print("  ✅ Extraction test: PASSED")
                else:
                    print("  ❌ Extraction test: FAILED")

        print("\nAll encryption algorithms tested successfully!")

    except Exception as e:
        print(f"❌ Error: {e}")
    finally:
        shutil.rmtree(temp_dir, ignore_errors=True)


def test_password_verification():
    """Test password verification"""
    print("\nTesting password verification...")

    temp_dir = tempfile.mkdtemp()

    try:
        # Create test file
        test_file = Path(temp_dir) / "secret.txt"
        test_file.write_text("This is secret content.")

        # Create encrypted zip using context manager
        with SecureZipper() as zipper:
            zipper.setpassword("correct_password")
            output_file = Path(temp_dir) / "secret.zip"
            zipper.create_zip(test_file, output_file)

        print(f"Created encrypted zip: {output_file}")

        # Test correct password
        with SecureZipper() as zipper:
            zipper.setpassword("correct_password")
            if zipper.test_zip_extraction(output_file):
                print("✅ Correct password: PASSED")
            else:
                print("❌ Correct password: FAILED")

        # Test wrong password
        with SecureZipper() as zipper:
            zipper.setpassword("wrong_password")
            if not zipper.test_zip_extraction(output_file):
                print("✅ Wrong password: CORRECTLY BLOCKED")
            else:
                print("❌ Wrong password: INCORRECTLY ALLOWED")

        # Test no password
        with SecureZipper() as zipper:
            if not zipper.test_zip_extraction(output_file):
                print("✅ No password: CORRECTLY BLOCKED")
            else:
                print("❌ No password: INCORRECTLY ALLOWED")

        print("Password verification tests completed!")

    except Exception as e:
        print(f"❌ Error: {e}")
    finally:
        shutil.rmtree(temp_dir, ignore_errors=True)


if __name__ == "__main__":
    print("🔐 MiniZipper - Encryption Tests")
    print("=" * 50)

    test_encryption_algorithms()
    test_password_verification()

    print("\n🎉 All tests completed!")
