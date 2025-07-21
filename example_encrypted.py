#!/usr/bin/env python3
"""
Encrypted Zip Example

This example demonstrates how to create and extract encrypted zip files
using different encryption algorithms.
"""

import shutil
import tempfile
from pathlib import Path

from minizipper import EncryptionAlgorithm, SecureZipper, ZipError


def create_test_data():
    """Create test data for encryption examples"""
    temp_dir = tempfile.mkdtemp()

    # Create test files with different content
    test_dir = Path(temp_dir) / "secret_data"
    test_dir.mkdir()

    # Create various types of files
    (test_dir / "document.txt").write_text("This is a confidential document.")
    (test_dir / "config.json").write_text('{"api_key": "secret123", "database": "prod"}')
    (test_dir / "image.jpg").write_bytes(b"fake_jpeg_data_here")
    (test_dir / "script.py").write_text("import os\nprint('Secret script')\n")

    # Create subdirectory with more files
    sub_dir = test_dir / "backup"
    sub_dir.mkdir()
    (sub_dir / "data.csv").write_text("id,name,email\n1,John,john@example.com\n")
    (sub_dir / "log.txt").write_text("2024-01-01: System started\n2024-01-01: Backup completed\n")

    return temp_dir, test_dir


def demonstrate_encryption_algorithms():
    """Demonstrate all available encryption algorithms"""
    print("=" * 70)
    print("Demonstrating All Encryption Algorithms")
    print("=" * 70)

    temp_dir, test_dir = create_test_data()

    try:
        # Use context manager for automatic cleanup
        with SecureZipper() as zipper:
            # Test all encryption algorithms
            algorithms = [
                (EncryptionAlgorithm.XOR, "Simple XOR encryption"),
                (EncryptionAlgorithm.HMAC_SHA256, "HMAC-SHA256 encryption"),
                (EncryptionAlgorithm.AES_LIKE, "AES-like encryption"),
                (EncryptionAlgorithm.DOUBLE_XOR, "Double XOR encryption"),
                (EncryptionAlgorithm.CUSTOM_HASH, "Custom hash encryption")
            ]

            results = []

            for algorithm, description in algorithms:
                print(f"\n🔐 Testing {algorithm.name}: {description}")

                # Set password and algorithm
                zipper.setpassword("secure_password_123", algorithm)

                # Create encrypted zip
                output_file = Path(temp_dir) / f"encrypted_{algorithm.value}.zip"
                result = zipper.create_zip(test_dir, output_file)

                # Get file size
                size_bytes = output_file.stat().st_size
                size_kb = size_bytes / 1024

                print(f"   ✅ Created: {result}")
                print(f"   📁 Size: {size_kb:.2f} KB")

                # Test extraction
                if zipper.test_zip_extraction(output_file):
                    print("   ✅ Extraction test: PASSED")
                else:
                    print("   ❌ Extraction test: FAILED")

                results.append((algorithm, output_file, size_bytes))

            # Compare file sizes
            print("\n📊 File Size Comparison:")
            print(f"{'Algorithm':<15} {'Size (KB)':<12} {'Relative':<10}")
            print("-" * 40)

            min_size = min(size for _, _, size in results)

            for algorithm, _, size in results:
                size_kb = size / 1024
                relative = size / min_size
                print(f"{algorithm.name:<15} {size_kb:<12.2f} {relative:<10.2f}x")

        print("✅ Context manager automatically cleaned up sensitive data")
        return results

    except Exception as e:
        print(f"❌ Error: {e}")
        return []
    finally:
        shutil.rmtree(temp_dir, ignore_errors=True)


def demonstrate_password_security():
    """Demonstrate password security features"""
    print("\n" + "=" * 70)
    print("Password Security Demonstration")
    print("=" * 70)

    temp_dir, test_dir = create_test_data()

    try:
        zipper = SecureZipper()

        # Create encrypted zip with password
        password = "my_secure_password_2024"
        zipper.setpassword(password, EncryptionAlgorithm.HMAC_SHA256)

        output_file = Path(temp_dir) / "secure_backup.zip"
        zipper.create_zip(test_dir, output_file)

        print(f"✅ Created encrypted zip: {output_file}")

        # Test 1: Correct password
        print("\n🔑 Test 1: Correct password")
        zipper.setpassword(password)

        if zipper.test_zip_extraction(output_file):
            print("   ✅ Extraction with correct password: SUCCESS")
        else:
            print("   ❌ Extraction with correct password: FAILED")

        # Test 2: Wrong password
        print("\n🔑 Test 2: Wrong password")
        zipper.setpassword("wrong_password")

        if not zipper.test_zip_extraction(output_file):
            print("   ✅ Extraction with wrong password: CORRECTLY BLOCKED")
        else:
            print("   ❌ Extraction with wrong password: INCORRECTLY ALLOWED")

        # Test 3: No password
        print("\n🔑 Test 3: No password")
        zipper.setpassword(None)

        if not zipper.test_zip_extraction(output_file):
            print("   ✅ Extraction without password: CORRECTLY BLOCKED")
        else:
            print("   ❌ Extraction without password: INCORRECTLY ALLOWED")

        # Test 4: Empty password
        print("\n🔑 Test 4: Empty password")
        zipper.setpassword("")

        if not zipper.test_zip_extraction(output_file):
            print("   ✅ Extraction with empty password: CORRECTLY BLOCKED")
        else:
            print("   ❌ Extraction with empty password: INCORRECTLY ALLOWED")

    except Exception as e:
        print(f"❌ Error: {e}")
    finally:
        shutil.rmtree(temp_dir, ignore_errors=True)


def demonstrate_algorithm_compatibility():
    """Demonstrate algorithm compatibility and auto-detection"""
    print("\n" + "=" * 70)
    print("Algorithm Compatibility Demonstration")
    print("=" * 70)

    temp_dir, test_dir = create_test_data()

    try:
        # Create encrypted zip with HMAC-SHA256
        zipper = SecureZipper()
        zipper.setpassword("testpass", EncryptionAlgorithm.HMAC_SHA256)

        output_file = Path(temp_dir) / "hmac_encrypted.zip"
        zipper.create_zip(test_dir, output_file)

        print(f"✅ Created HMAC-SHA256 encrypted zip: {output_file}")

        # Test extraction with different algorithms (should auto-detect)
        test_algorithms = [
            EncryptionAlgorithm.XOR,
            EncryptionAlgorithm.AES_LIKE,
            EncryptionAlgorithm.DOUBLE_XOR,
            EncryptionAlgorithm.CUSTOM_HASH
        ]

        print("\n🔄 Testing extraction with different algorithms:")

        for alg in test_algorithms:
            zipper.setpassword("testpass", alg)

            if zipper.test_zip_extraction(output_file):
                print(f"   ✅ {alg.name}: SUCCESS (auto-detected)")
            else:
                print(f"   ❌ {alg.name}: FAILED")

        # Test extraction with wrong password
        print("\n🔑 Testing with wrong password:")
        zipper.setpassword("wrongpass", EncryptionAlgorithm.XOR)

        if not zipper.test_zip_extraction(output_file):
            print("   ✅ Wrong password: CORRECTLY BLOCKED")
        else:
            print("   ❌ Wrong password: INCORRECTLY ALLOWED")

    except Exception as e:
        print(f"❌ Error: {e}")
    finally:
        shutil.rmtree(temp_dir, ignore_errors=True)


def demonstrate_real_world_scenarios():
    """Demonstrate real-world usage scenarios"""
    print("\n" + "=" * 70)
    print("Real-World Usage Scenarios")
    print("=" * 70)

    temp_dir, test_dir = create_test_data()

    try:
        zipper = SecureZipper()

        # Scenario 1: Backup sensitive documents
        print("\n📁 Scenario 1: Backup sensitive documents")
        zipper.setpassword("backup_password_2024", EncryptionAlgorithm.HMAC_SHA256)

        backup_file = Path(temp_dir) / "sensitive_backup.zip"
        zipper.create_zip(test_dir, backup_file)

        print(f"   ✅ Created secure backup: {backup_file}")
        print(f"   📊 Size: {backup_file.stat().st_size / 1024:.2f} KB")

        # Scenario 2: Secure file transfer
        print("\n📤 Scenario 2: Secure file transfer")
        zipper.setpassword("transfer_key_123", EncryptionAlgorithm.AES_LIKE)

        transfer_file = Path(temp_dir) / "secure_transfer.zip"
        zipper.create_zip(test_dir, transfer_file)

        print(f"   ✅ Created transfer file: {transfer_file}")

        # Simulate transfer and extraction
        extract_dir = Path(temp_dir) / "received_files"
        if zipper.extract_zip(transfer_file, extract_dir):
            print(f"   ✅ Successfully extracted to: {extract_dir}")

            # List extracted files
            for item in extract_dir.rglob("*"):
                if item.is_file():
                    print(f"      📄 {item.relative_to(extract_dir)}")
        else:
            print("   ❌ Extraction failed")

        # Scenario 3: Quick encryption for temporary files
        print("\n⚡ Scenario 3: Quick encryption for temporary files")
        zipper.setpassword("temp123", EncryptionAlgorithm.XOR)  # Fast algorithm

        temp_secure_file = Path(temp_dir) / "temp_secure.zip"
        zipper.create_zip(test_dir, temp_secure_file)

        print(f"   ✅ Created temporary secure file: {temp_secure_file}")

        # Scenario 4: Maximum security for critical data
        print("\n🔒 Scenario 4: Maximum security for critical data")
        zipper.setpassword("critical_data_key_2024", EncryptionAlgorithm.CUSTOM_HASH)

        critical_file = Path(temp_dir) / "critical_data.zip"
        zipper.create_zip(test_dir, critical_file)

        print(f"   ✅ Created critical data file: {critical_file}")

        # Verify all files can be extracted
        print("\n🔍 Verifying all scenarios:")
        scenarios = [
            ("Backup", backup_file, "backup_password_2024"),
            ("Transfer", transfer_file, "transfer_key_123"),
            ("Temporary", temp_secure_file, "temp123"),
            ("Critical", critical_file, "critical_data_key_2024")
        ]

        for name, file_path, password in scenarios:
            zipper.setpassword(password)
            if zipper.test_zip_extraction(file_path):
                print(f"   ✅ {name}: VERIFIED")
            else:
                print(f"   ❌ {name}: FAILED")

    except Exception as e:
        print(f"❌ Error: {e}")
    finally:
        shutil.rmtree(temp_dir, ignore_errors=True)


def demonstrate_error_handling():
    """Demonstrate error handling in encrypted operations"""
    print("\n" + "=" * 70)
    print("Error Handling Demonstration")
    print("=" * 70)

    temp_dir, test_dir = create_test_data()

    try:
        zipper = SecureZipper()

        # Create a valid encrypted zip
        zipper.setpassword("testpass")
        valid_file = Path(temp_dir) / "valid.zip"
        zipper.create_zip(test_dir, valid_file)

        print(f"✅ Created valid encrypted zip: {valid_file}")

        # Test various error conditions
        print("\n🚨 Testing error conditions:")

        # 1. Try to extract with wrong password
        print("\n1. Wrong password:")
        zipper.setpassword("wrongpass")
        if not zipper.extract_zip(valid_file, Path(temp_dir) / "wrong_pass"):
            print("   ✅ Correctly handled wrong password")
        else:
            print("   ❌ Incorrectly allowed wrong password")

        # 2. Try to extract without password
        print("\n2. No password:")
        zipper.setpassword(None)
        if not zipper.extract_zip(valid_file, Path(temp_dir) / "no_pass"):
            print("   ✅ Correctly handled no password")
        else:
            print("   ❌ Incorrectly allowed no password")

        # 3. Try to extract non-existent file
        print("\n3. Non-existent file:")
        non_existent = Path(temp_dir) / "nonexistent.zip"
        if not zipper.extract_zip(non_existent, Path(temp_dir) / "extract_nonexistent"):
            print("   ✅ Correctly handled non-existent file")
        else:
            print("   ❌ Incorrectly handled non-existent file")

        # 4. Try to create encrypted zip with empty password
        print("\n4. Empty password:")
        try:
            zipper.setpassword("")
            zipper.create_zip(test_dir, Path(temp_dir) / "empty_pass.zip")
            print("   ❌ Incorrectly allowed empty password")
        except ZipError as e:
            print(f"   ✅ Correctly caught empty password error: {e}")

        # 5. Try to extract to non-writable directory
        print("\n5. Non-writable directory:")
        zipper.setpassword("testpass")
        non_writable = Path("/root/non_writable_dir")  # Should fail
        if not zipper.extract_zip(valid_file, non_writable):
            print("   ✅ Correctly handled non-writable directory")
        else:
            print("   ❌ Incorrectly handled non-writable directory")

    except Exception as e:
        print(f"❌ Error: {e}")
    finally:
        shutil.rmtree(temp_dir, ignore_errors=True)


def main():
    """Main function to run all encrypted zip demonstrations"""
    print("🔐 MiniZipper - Encrypted File Examples")
    print("This script demonstrates encrypted zip functionality with various algorithms.")

    # Run all demonstrations
    demonstrate_encryption_algorithms()
    demonstrate_password_security()
    demonstrate_algorithm_compatibility()
    demonstrate_real_world_scenarios()
    demonstrate_error_handling()

    print("\n" + "=" * 70)
    print("🎉 All encrypted zip demonstrations completed!")
    print("=" * 70)
    print("\n💡 Key takeaways:")
    print("   • Different algorithms offer different security levels")
    print("   • HMAC-SHA256 provides high security with salt")
    print("   • XOR is fast but basic security")
    print("   • Algorithm auto-detection ensures compatibility")
    print("   • Password verification prevents unauthorized access")


if __name__ == "__main__":
    main()
