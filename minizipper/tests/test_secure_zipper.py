"""
Tests for SecureZipper module
"""

import shutil
import tempfile
from pathlib import Path

import pytest

from minizipper.secure_zipper import EncryptionAlgorithm, SecureZipper, ZipError


class TestSecureZipper:
    """Test cases for SecureZipper class"""

    def setup_method(self):
        """Set up test environment"""
        self.temp_dir = tempfile.mkdtemp()
        self.zipper = SecureZipper()

    def teardown_method(self):
        """Clean up test environment"""
        shutil.rmtree(self.temp_dir, ignore_errors=True)

    def test_init(self):
        """Test SecureZipper initialization"""
        zipper = SecureZipper()
        assert zipper.compression_level == 6
        assert zipper._password is None
        assert zipper._encryption_algorithm == EncryptionAlgorithm.XOR

        zipper = SecureZipper(compression_level=9)
        assert zipper.compression_level == 9

    def test_init_invalid_compression_level(self):
        """Test initialization with invalid compression level"""
        with pytest.raises(ValueError, match="Compression level must be between 0-9"):
            SecureZipper(compression_level=10)

        with pytest.raises(ValueError, match="Compression level must be between 0-9"):
            SecureZipper(compression_level=-1)

    def test_setpassword(self):
        """Test password setting"""
        # Test setting password
        self.zipper.setpassword("testpass")
        assert self.zipper._password == "testpass"
        assert self.zipper._encryption_algorithm == EncryptionAlgorithm.XOR

        # Test setting password with algorithm
        self.zipper.setpassword("testpass2", EncryptionAlgorithm.HMAC_SHA256)
        assert self.zipper._password == "testpass2"
        assert self.zipper._encryption_algorithm == EncryptionAlgorithm.HMAC_SHA256

        # Test disabling encryption
        self.zipper.setpassword(None)
        assert self.zipper._password is None

        self.zipper.setpassword("")
        assert self.zipper._password is None

    def test_create_zip_single_file(self):
        """Test creating zip from single file"""
        # Create test file
        test_file = Path(self.temp_dir) / "test.txt"
        test_file.write_text("Hello, World!")

        # Create zip
        output_file = Path(self.temp_dir) / "output.zip"
        result = self.zipper.create_zip(test_file, output_file)

        assert result == str(output_file)
        assert output_file.exists()

    def test_create_zip_directory(self):
        """Test creating zip from directory"""
        # Create test directory structure
        test_dir = Path(self.temp_dir) / "test_dir"
        test_dir.mkdir()

        (test_dir / "file1.txt").write_text("File 1")
        (test_dir / "file2.txt").write_text("File 2")
        (test_dir / "subdir").mkdir()
        (test_dir / "subdir" / "file3.txt").write_text("File 3")

        # Create zip
        output_file = Path(self.temp_dir) / "output.zip"
        result = self.zipper.create_zip(test_dir, output_file)

        assert result == str(output_file)
        assert output_file.exists()

    def test_create_zip_with_hidden_files(self):
        """Test creating zip with hidden files"""
        # Create test directory with hidden files
        test_dir = Path(self.temp_dir) / "test_dir"
        test_dir.mkdir()

        (test_dir / "file1.txt").write_text("File 1")
        (test_dir / ".hidden.txt").write_text("Hidden file")

        # Create zip without hidden files
        output_file1 = Path(self.temp_dir) / "output1.zip"
        self.zipper.create_zip(test_dir, output_file1, include_hidden=False)

        # Create zip with hidden files
        output_file2 = Path(self.temp_dir) / "output2.zip"
        self.zipper.create_zip(test_dir, output_file2, include_hidden=True)

        # Check file sizes (with hidden files should be larger)
        assert output_file2.stat().st_size > output_file1.stat().st_size

    def test_create_zip_from_files(self):
        """Test creating zip from multiple files"""
        # Create test files
        files = []
        for i in range(3):
            file_path = Path(self.temp_dir) / f"file{i}.txt"
            file_path.write_text(f"Content {i}")
            files.append(file_path)

        # Create zip
        output_file = Path(self.temp_dir) / "output.zip"
        result = self.zipper.create_zip_from_files(files, output_file)

        assert result == str(output_file)
        assert output_file.exists()

    def test_create_zip_from_files_with_base_dir(self):
        """Test creating zip from files with base directory"""
        # Create test directory structure
        base_dir = Path(self.temp_dir) / "base"
        base_dir.mkdir()

        (base_dir / "file1.txt").write_text("File 1")
        (base_dir / "file2.txt").write_text("File 2")

        files = [base_dir / "file1.txt", base_dir / "file2.txt"]

        # Create zip with base directory
        output_file = Path(self.temp_dir) / "output.zip"
        result = self.zipper.create_zip_from_files(files, output_file, base_dir=base_dir)

        assert result == str(output_file)
        assert output_file.exists()

    def test_create_encrypted_zip(self):
        """Test creating encrypted zip"""
        # Create test file
        test_file = Path(self.temp_dir) / "test.txt"
        test_file.write_text("Secret content")

        # Set password
        self.zipper.setpassword("secretpass")

        # Create encrypted zip
        output_file = Path(self.temp_dir) / "encrypted.zip"
        result = self.zipper.create_zip(test_file, output_file)

        assert result == str(output_file)
        assert output_file.exists()

        # Verify it's encrypted (should be larger than standard zip)
        standard_output = Path(self.temp_dir) / "standard.zip"
        self.zipper.setpassword(None)
        self.zipper.create_zip(test_file, standard_output)

        assert output_file.stat().st_size > standard_output.stat().st_size

    def test_create_encrypted_zip_with_different_algorithms(self):
        """Test creating encrypted zip with different algorithms"""
        # Create test file
        test_file = Path(self.temp_dir) / "test.txt"
        test_file.write_text("Test content")

        algorithms = [
            EncryptionAlgorithm.XOR,
            EncryptionAlgorithm.HMAC_SHA256,
            EncryptionAlgorithm.AES_LIKE,
            EncryptionAlgorithm.DOUBLE_XOR,
            EncryptionAlgorithm.CUSTOM_HASH
        ]

        for alg in algorithms:
            self.zipper.setpassword("testpass", alg)
            output_file = Path(self.temp_dir) / f"test_{alg.value}.zip"
            result = self.zipper.create_zip(test_file, output_file)

            assert result == str(output_file)
            assert output_file.exists()

    def test_extract_standard_zip(self):
        """Test extracting standard zip"""
        # Create test file and zip
        test_file = Path(self.temp_dir) / "test.txt"
        test_file.write_text("Extract test content")

        zip_file = Path(self.temp_dir) / "test.zip"
        self.zipper.create_zip(test_file, zip_file)

        # Extract
        extract_dir = Path(self.temp_dir) / "extracted"
        success = self.zipper.extract_zip(zip_file, extract_dir)

        assert success
        assert (extract_dir / "test.txt").exists()
        assert (extract_dir / "test.txt").read_text() == "Extract test content"

    def test_extract_encrypted_zip(self):
        """Test extracting encrypted zip"""
        # Create test file and encrypted zip
        test_file = Path(self.temp_dir) / "test.txt"
        test_file.write_text("Encrypted content")

        self.zipper.setpassword("testpass")
        zip_file = Path(self.temp_dir) / "encrypted.zip"
        self.zipper.create_zip(test_file, zip_file)

        # Extract
        extract_dir = Path(self.temp_dir) / "extracted"
        success = self.zipper.extract_zip(zip_file, extract_dir)

        assert success
        assert (extract_dir / "test.txt").exists()
        assert (extract_dir / "test.txt").read_text() == "Encrypted content"

    def test_test_zip_extraction(self):
        """Test zip extraction testing"""
        # Create test file and zip
        test_file = Path(self.temp_dir) / "test.txt"
        test_file.write_text("Test content")

        zip_file = Path(self.temp_dir) / "test.zip"
        self.zipper.create_zip(test_file, zip_file)

        # Test extraction
        assert self.zipper.test_zip_extraction(zip_file)

    def test_test_encrypted_zip_extraction(self):
        """Test encrypted zip extraction testing"""
        # Create test file and encrypted zip
        test_file = Path(self.temp_dir) / "test.txt"
        test_file.write_text("Test content")

        self.zipper.setpassword("testpass")
        zip_file = Path(self.temp_dir) / "encrypted.zip"
        self.zipper.create_zip(test_file, zip_file)

        # Test extraction
        assert self.zipper.test_zip_extraction(zip_file)

    def test_error_handling(self):
        """Test error handling"""
        # Test non-existent source
        with pytest.raises(ZipError, match="Source path does not exist"):
            self.zipper.create_zip("/nonexistent/file.txt", "output.zip")

        # Test empty file list
        with pytest.raises(ZipError, match="File list cannot be empty"):
            self.zipper.create_zip_from_files([], "output.zip")

        # Test non-existent file in list
        with pytest.raises(ZipError, match="File does not exist"):
            self.zipper.create_zip_from_files(["/nonexistent/file.txt"], "output.zip")

        # Test non-existent zip for extraction
        assert not self.zipper.extract_zip("/nonexistent.zip", "extract_dir")

    def test_encryption_without_password(self):
        """Test encryption without password"""
        # Create test file
        test_file = Path(self.temp_dir) / "test.txt"
        test_file.write_text("Test content")

        # Set empty password (should disable encryption)
        self.zipper.setpassword("")

        # Should create standard zip (not encrypted)
        output_file = Path(self.temp_dir) / "output.zip"
        result = self.zipper.create_zip(test_file, output_file)

        # Verify it's a standard zip, not encrypted
        assert result == str(output_file)
        assert output_file.exists()

        # Test that it's not encrypted by trying to extract without password
        extract_dir = Path(self.temp_dir) / "extracted"
        success = self.zipper.extract_zip(output_file, extract_dir)
        assert success
        assert (extract_dir / "test.txt").read_text() == "Test content"

    def test_algorithm_compatibility(self):
        """Test algorithm compatibility"""
        # Create test file
        test_file = Path(self.temp_dir) / "test.txt"
        test_file.write_text("Compatibility test")

        # Create encrypted zip with one algorithm
        self.zipper.setpassword("testpass", EncryptionAlgorithm.HMAC_SHA256)
        zip_file = Path(self.temp_dir) / "test.zip"
        self.zipper.create_zip(test_file, zip_file)

        # Try to extract with different algorithm (should work due to auto-detection)
        self.zipper.setpassword("testpass", EncryptionAlgorithm.XOR)
        extract_dir = Path(self.temp_dir) / "extracted"
        success = self.zipper.extract_zip(zip_file, extract_dir)

        assert success
        assert (extract_dir / "test.txt").read_text() == "Compatibility test"

    def test_context_manager_basic(self):
        """Test basic context manager functionality"""
        # Create test file
        test_file = Path(self.temp_dir) / "test.txt"
        test_file.write_text("Context manager test")

        # Test with context manager
        with SecureZipper() as zipper:
            zipper.setpassword("testpass", EncryptionAlgorithm.HMAC_SHA256)
            output_file = Path(self.temp_dir) / "context_test.zip"
            result = zipper.create_zip(test_file, output_file)

            assert result == str(output_file)
            assert output_file.exists()
            assert zipper._password == "testpass"
            assert zipper._encryption_algorithm == EncryptionAlgorithm.HMAC_SHA256

        # Verify sensitive data is cleared after context exit
        assert zipper._password is None
        assert zipper._encryption_algorithm == EncryptionAlgorithm.XOR

    def test_context_manager_exception_handling(self):
        """Test context manager exception handling"""
        try:
            with SecureZipper() as zipper:
                zipper.setpassword("testpass")
                # This should raise an exception
                zipper.create_zip("/nonexistent/file.txt", "output.zip")
        except ZipError:
            # Exception should be raised
            pass
        else:
            pytest.fail("Expected ZipError to be raised")

    def test_context_manager_multiple_instances(self):
        """Test multiple context manager instances"""
        test_file = Path(self.temp_dir) / "test.txt"
        test_file.write_text("Multiple instances test")

        # First context manager
        with SecureZipper() as zipper1:
            zipper1.setpassword("pass1", EncryptionAlgorithm.XOR)
            output1 = Path(self.temp_dir) / "test1.zip"
            zipper1.create_zip(test_file, output1)
            assert output1.exists()

        # Second context manager
        with SecureZipper() as zipper2:
            zipper2.setpassword("pass2", EncryptionAlgorithm.HMAC_SHA256)
            output2 = Path(self.temp_dir) / "test2.zip"
            zipper2.create_zip(test_file, output2)
            assert output2.exists()

        # Verify both instances are independent
        assert zipper1._password is None
        assert zipper2._password is None

    def test_context_manager_nested(self):
        """Test nested context managers"""
        test_file = Path(self.temp_dir) / "test.txt"
        test_file.write_text("Nested context test")

        with SecureZipper() as outer_zipper:
            outer_zipper.setpassword("outer_pass")

            with SecureZipper() as inner_zipper:
                inner_zipper.setpassword("inner_pass")
                output_inner = Path(self.temp_dir) / "inner.zip"
                inner_zipper.create_zip(test_file, output_inner)
                assert output_inner.exists()
                assert inner_zipper._password == "inner_pass"

            # Inner context should be cleaned up
            assert inner_zipper._password is None

            output_outer = Path(self.temp_dir) / "outer.zip"
            outer_zipper.create_zip(test_file, output_outer)
            assert output_outer.exists()
            assert outer_zipper._password == "outer_pass"

        # Both contexts should be cleaned up
        assert outer_zipper._password is None
        assert inner_zipper._password is None

    def test_context_manager_vs_traditional(self):
        """Test context manager vs traditional usage produces same results"""
        test_file = Path(self.temp_dir) / "test.txt"
        test_file.write_text("Comparison test")

        # Traditional usage
        zipper_traditional = SecureZipper()
        zipper_traditional.setpassword("testpass")
        output_traditional = Path(self.temp_dir) / "traditional.zip"
        result_traditional = zipper_traditional.create_zip(test_file, output_traditional)

        # Context manager usage
        with SecureZipper() as zipper_context:
            zipper_context.setpassword("testpass")
            output_context = Path(self.temp_dir) / "context.zip"
            result_context = zipper_context.create_zip(test_file, output_context)

        # Both should produce identical results
        assert result_traditional == str(output_traditional)
        assert result_context == str(output_context)
        assert output_traditional.exists()
        assert output_context.exists()
        assert output_traditional.stat().st_size == output_context.stat().st_size
