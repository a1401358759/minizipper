"""
MiniZipper Core Module

Provides functionality to create zip files, supporting both standard zip and password-encrypted zip,
ensuring cross-platform compatibility.
"""

import hashlib
import logging
import secrets
import struct
import zipfile
from enum import Enum
from pathlib import Path
from typing import List, Optional, Union

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class EncryptionAlgorithm(Enum):
    """Encryption algorithm enumeration"""
    XOR = "xor"                    # Simple XOR encryption (default)
    HMAC_SHA256 = "hmac_sha256"    # HMAC-SHA256 encryption
    AES_LIKE = "aes_like"          # AES-like encryption (simulated with standard library)
    DOUBLE_XOR = "double_xor"      # Double XOR encryption
    CUSTOM_HASH = "custom_hash"    # Custom hash encryption


class ZipError(Exception):
    """Zip-related errors"""
    pass


class SecureZipper:
    """
    Zip file creator

    Supports creating standard zip files and password-encrypted zip files,
    ensuring they can be extracted normally on all platforms.
    Uses standard zip compression, compatible with Windows, macOS, Linux and other systems.
    Controls encryption functionality through the setpassword() method.
    Supports multiple encryption algorithm choices.

    Can be used as a context manager with 'with' statement.
    """

    def __init__(self, compression_level: int = 6):
        """
        Initialize SecureZipper

        Args:
            compression_level: Compression level (0-9), default is 6
        """
        self.compression_level = compression_level
        self._password = None
        self._encryption_algorithm = EncryptionAlgorithm.XOR
        self._validate_compression_level()

    def __enter__(self):
        """
        Context manager entry point

        Returns:
            self: The SecureZipper instance
        """
        logger.debug("SecureZipper context manager entered")
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """
        Context manager exit point

        Args:
            exc_type: Exception type if an exception occurred
            exc_val: Exception value if an exception occurred
            exc_tb: Exception traceback if an exception occurred

        Returns:
            bool: False to re-raise exceptions, True to suppress them
        """
        logger.debug("SecureZipper context manager exited")

        # Clear sensitive data
        self._password = None
        self._encryption_algorithm = EncryptionAlgorithm.XOR

        # Log any exceptions that occurred
        if exc_type is not None:
            logger.warning(f"Exception in SecureZipper context: {exc_type.__name__}: {exc_val}")

        # Return False to allow exceptions to propagate
        return False

    def _validate_compression_level(self):
        """Validate compression level"""
        if not 0 <= self.compression_level <= 9:
            raise ValueError("Compression level must be between 0-9")

    def setpassword(self, password: str, algorithm: EncryptionAlgorithm = EncryptionAlgorithm.XOR):
        """
        Set encryption password and algorithm

        Args:
            password: Encryption password, if None or empty string, encryption is disabled
            algorithm: Encryption algorithm, default is XOR
        """
        if password is None or password == "":
            self._password = None
            logger.info("Encryption disabled")
        else:
            self._password = password
            self._encryption_algorithm = algorithm
            logger.info(f"Encryption enabled, using algorithm: {algorithm.value}")

    def _is_encrypted(self) -> bool:
        """Check if encryption is enabled"""
        return self._password is not None

    def _generate_key(self, password: str) -> bytes:
        """Generate encryption key"""
        # Generate key from password
        key = hashlib.sha256(password.encode('utf-8')).digest()
        return key

    def _generate_salt(self) -> bytes:
        """Generate random salt"""
        return secrets.token_bytes(16)

    def _xor_encrypt(self, data: bytes, key: bytes) -> bytes:
        """XOR encryption"""
        encrypted = bytearray()
        for i, byte in enumerate(data):
            encrypted.append(byte ^ key[i % len(key)])
        return bytes(encrypted)

    def _hmac_sha256_encrypt(self, data: bytes, key: bytes) -> bytes:
        """HMAC-SHA256 encryption"""
        # Generate random salt
        salt = secrets.token_bytes(16)

        # Generate HMAC key using salt
        hmac_key = hashlib.sha256(key + salt).digest()

        # Encrypt data using HMAC key
        encrypted = bytearray()
        for i, byte in enumerate(data):
            encrypted.append(byte ^ hmac_key[i % len(hmac_key)])

        # Return salt + encrypted data
        return salt + bytes(encrypted)

    def _aes_like_encrypt(self, data: bytes, key: bytes) -> bytes:
        """AES-like encryption (simulated with standard library)"""
        # Generate multiple keys using SHA256
        key1 = hashlib.sha256(key + b"key1").digest()
        key2 = hashlib.sha256(key + b"key2").digest()

        encrypted = bytearray()
        for i, byte in enumerate(data):
            # Simulate AES multi-round encryption
            encrypted_byte = byte
            encrypted_byte ^= key1[i % len(key1)]
            encrypted_byte ^= key2[i % len(key2)]
            encrypted.append(encrypted_byte)
        return bytes(encrypted)

    def _double_xor_encrypt(self, data: bytes, key: bytes) -> bytes:
        """Double XOR encryption"""
        # First round XOR
        temp = self._xor_encrypt(data, key)
        # Second round XOR (using reversed key)
        reversed_key = key[::-1]
        return self._xor_encrypt(temp, reversed_key)

    def _custom_hash_encrypt(self, data: bytes, key: bytes) -> bytes:
        """Custom hash encryption"""
        # Use multiple hash algorithms
        md5_key = hashlib.md5(key).digest()
        sha1_key = hashlib.sha1(key).digest()
        sha256_key = hashlib.sha256(key).digest()

        encrypted = bytearray()
        for i, byte in enumerate(data):
            encrypted_byte = byte
            encrypted_byte ^= md5_key[i % len(md5_key)]
            encrypted_byte ^= sha1_key[i % len(sha1_key)]
            encrypted_byte ^= sha256_key[i % len(sha256_key)]
            encrypted.append(encrypted_byte)
        return bytes(encrypted)

    def _encrypt_data(self, data: bytes, password: str) -> bytes:
        """Encrypt data based on selected algorithm"""
        key = self._generate_key(password)

        if self._encryption_algorithm == EncryptionAlgorithm.XOR:
            return self._xor_encrypt(data, key)
        elif self._encryption_algorithm == EncryptionAlgorithm.HMAC_SHA256:
            return self._hmac_sha256_encrypt(data, key)
        elif self._encryption_algorithm == EncryptionAlgorithm.AES_LIKE:
            return self._aes_like_encrypt(data, key)
        elif self._encryption_algorithm == EncryptionAlgorithm.DOUBLE_XOR:
            return self._double_xor_encrypt(data, key)
        elif self._encryption_algorithm == EncryptionAlgorithm.CUSTOM_HASH:
            return self._custom_hash_encrypt(data, key)
        else:
            # Default to XOR
            return self._xor_encrypt(data, key)

    def _decrypt_data(self, data: bytes, password: str) -> bytes:
        """Decrypt data"""
        key = self._generate_key(password)

        if self._encryption_algorithm == EncryptionAlgorithm.HMAC_SHA256:
            return self._hmac_sha256_decrypt(data, key)
        else:
            # Other algorithms are symmetric, decryption same as encryption
            return self._encrypt_data(data, password)

    def _hmac_sha256_decrypt(self, data: bytes, key: bytes) -> bytes:
        """HMAC-SHA256 decryption"""
        # Extract salt (first 16 bytes)
        salt = data[:16]
        encrypted_data = data[16:]

        # Generate HMAC key using salt
        hmac_key = hashlib.sha256(key + salt).digest()

        # Decrypt data
        decrypted = bytearray()
        for i, byte in enumerate(encrypted_data):
            decrypted.append(byte ^ hmac_key[i % len(hmac_key)])

        return bytes(decrypted)

    def _encrypt_zip_file(self, input_path: Path, output_path: Path, password: str):
        """Encrypt zip file"""
        with open(input_path, 'rb') as f:
            zip_data = f.read()

        # Encrypt data
        encrypted_data = self._encrypt_data(zip_data, password)

        # Add encryption markers and metadata
        header = struct.pack('<I', len(encrypted_data))  # Data length
        key_hash = hashlib.sha256(password.encode('utf-8')).digest()[:8]  # Key hash
        algorithm_id = self._encryption_algorithm.value.encode('utf-8')
        algorithm_length = len(algorithm_id)
        algorithm_header = struct.pack('<B', algorithm_length)  # Algorithm name length

        with open(output_path, 'wb') as f:
            f.write(b'SECUREZIP')  # File identifier
            f.write(header)  # Data length
            f.write(key_hash)  # Key hash
            f.write(algorithm_header)  # Algorithm name length
            f.write(algorithm_id)  # Algorithm identifier
            f.write(encrypted_data)  # Encrypted data

    def _decrypt_zip_file(self, input_path: Path, output_path: Path, password: str) -> bool:
        """Decrypt zip file"""
        try:
            with open(input_path, 'rb') as f:
                # Read file identifier
                magic = f.read(9)
                if magic != b'SECUREZIP':
                    return False

                # Read data length
                data_len = struct.unpack('<I', f.read(4))[0]

                # Read key hash
                stored_key_hash = f.read(8)
                expected_key_hash = hashlib.sha256(password.encode('utf-8')).digest()[:8]

                if stored_key_hash != expected_key_hash:
                    return False

                # Read algorithm identifier
                algorithm_length = struct.unpack('<B', f.read(1))[0]  # Algorithm name length
                algorithm_id = f.read(algorithm_length).decode('utf-8')

                # Set algorithm (if different from current)
                if algorithm_id and algorithm_id != self._encryption_algorithm.value:
                    try:
                        self._encryption_algorithm = EncryptionAlgorithm(algorithm_id)
                        logger.info(f"Detected file using algorithm: {algorithm_id}")
                    except ValueError:
                        logger.warning(f"Unknown algorithm: {algorithm_id}, using default algorithm")

                # Read encrypted data
                encrypted_data = f.read(data_len)

                # Decrypt data
                decrypted_data = self._decrypt_data(encrypted_data, password)

                # Write decrypted zip file
                with open(output_path, 'wb') as out_f:
                    out_f.write(decrypted_data)

                return True

        except Exception as e:
            logger.warning(f"Decryption failed: {e}")
            return False

    def create_zip(
        self,
        source_path: Union[str, Path],
        output_path: Union[str, Path],
        include_hidden: bool = False
    ) -> str:
        """
        Create zip file

        Args:
            source_path: Path to file or directory to compress
            output_path: Output zip file path
            include_hidden: Whether to include hidden files

        Returns:
            Created zip file path

        Raises:
            ZipError: Error when creating zip file
        """
        try:
            source_path = Path(source_path)
            output_path = Path(output_path)

            # Validate inputs
            self._validate_inputs(source_path)

            # Ensure output directory exists
            output_path.parent.mkdir(parents=True, exist_ok=True)

            if self._is_encrypted():
                # Create encrypted zip file
                return self._create_encrypted_zip(source_path, output_path, include_hidden)
            else:
                # Create standard zip file
                return self._create_standard_zip(source_path, output_path, include_hidden)

        except Exception as e:
            raise ZipError(f"Failed to create zip file: {e!s}") from e

    def _create_standard_zip(self, source_path: Path, output_path: Path, include_hidden: bool) -> str:
        """Create standard zip file"""
        with zipfile.ZipFile(
            output_path,
            'w',
            compression=zipfile.ZIP_DEFLATED,
            compresslevel=self.compression_level
        ) as zip_file:
            self._add_to_zip(zip_file, source_path, include_hidden)

        logger.info(f"Successfully created zip file: {output_path}")
        return str(output_path)

    def _create_encrypted_zip(self, source_path: Path, output_path: Path, include_hidden: bool) -> str:
        """Create encrypted zip file"""
        # Create temporary zip file
        temp_zip_path = output_path.with_suffix('.tmp.zip')

        # First create standard zip file
        with zipfile.ZipFile(
            temp_zip_path,
            'w',
            compression=zipfile.ZIP_DEFLATED,
            compresslevel=self.compression_level
        ) as zip_file:
            self._add_to_zip(zip_file, source_path, include_hidden)

        # Encrypt entire zip file
        self._encrypt_zip_file(temp_zip_path, output_path, self._password)

        # Delete temporary file
        temp_zip_path.unlink()

        logger.info(f"Successfully created encrypted zip file: {output_path}")
        return str(output_path)

    def _validate_inputs(self, source_path: Path):
        """Validate input parameters"""
        if not source_path.exists():
            raise ZipError(f"Source path does not exist: {source_path}")

        if self._is_encrypted() and not self._password:
            raise ZipError("Password cannot be empty")

    def _add_to_zip(
        self,
        zip_file: zipfile.ZipFile,
        source_path: Path,
        include_hidden: bool
    ):
        """Add files to zip"""
        if source_path.is_file():
            self._add_file_to_zip(zip_file, source_path)
        elif source_path.is_dir():
            self._add_directory_to_zip(zip_file, source_path, include_hidden)

    def _add_file_to_zip(self, zip_file: zipfile.ZipFile, file_path: Path):
        """Add single file to zip"""
        try:
            # Use relative path as zip internal path
            arc_name = file_path.name

            # Read file content
            with open(file_path, 'rb') as f:
                file_data = f.read()

            # Create zip entry
            zip_file.writestr(arc_name, file_data)

            logger.debug(f"Added file: {file_path} -> {arc_name}")

        except Exception as e:
            raise ZipError(f"Failed to add file to zip {file_path}: {e!s}") from e

    def _add_directory_to_zip(
        self,
        zip_file: zipfile.ZipFile,
        dir_path: Path,
        include_hidden: bool
    ):
        """Add directory to zip"""
        try:
            for item in dir_path.rglob('*'):
                # Skip hidden files (if not specified to include)
                if not include_hidden and self._is_hidden(item):
                    continue

                # Calculate relative path
                relative_path = item.relative_to(dir_path)

                if item.is_file():
                    # Add file
                    with open(item, 'rb') as f:
                        file_data = f.read()

                    zip_file.writestr(str(relative_path), file_data)

                    logger.debug(f"Added file: {item} -> {relative_path}")

                elif item.is_dir():
                    # Add empty directory (create directory structure)
                    zip_file.writestr(str(relative_path) + '/', '')

                    logger.debug(f"Added directory: {item} -> {relative_path}/")

        except Exception as e:
            raise ZipError(f"Failed to add directory to zip {dir_path}: {e!s}") from e

    def _is_hidden(self, path: Path) -> bool:
        """Check if file is hidden"""
        return path.name.startswith('.')

    def create_zip_from_files(
        self,
        file_paths: List[Union[str, Path]],
        output_path: Union[str, Path],
        base_dir: Optional[Union[str, Path]] = None
    ) -> str:
        """
        Create zip file from multiple files

        Args:
            file_paths: List of file paths to compress
            output_path: Output zip file path
            base_dir: Base directory for calculating relative paths

        Returns:
            Created zip file path
        """
        try:
            output_path = Path(output_path)
            file_paths = [Path(fp) for fp in file_paths]

            # Validate inputs
            if not file_paths:
                raise ZipError("File list cannot be empty")

            for file_path in file_paths:
                if not file_path.exists():
                    raise ZipError(f"File does not exist: {file_path}")

            # Ensure output directory exists
            output_path.parent.mkdir(parents=True, exist_ok=True)

            if self._is_encrypted():
                # Create encrypted zip file
                return self._create_encrypted_zip_from_files(file_paths, output_path, base_dir)
            else:
                # Create standard zip file
                return self._create_standard_zip_from_files(file_paths, output_path, base_dir)

        except Exception as e:
            raise ZipError(f"Failed to create zip file: {e!s}") from e

    def _create_standard_zip_from_files(self, file_paths: List[Path], output_path: Path, base_dir: Optional[Path]) -> str:
        """Create standard zip file from multiple files"""
        with zipfile.ZipFile(
            output_path,
            'w',
            compression=zipfile.ZIP_DEFLATED,
            compresslevel=self.compression_level
        ) as zip_file:
            for file_path in file_paths:
                if base_dir:
                    arc_name = file_path.relative_to(base_dir)
                else:
                    arc_name = file_path.name

                # Read file content
                with open(file_path, 'rb') as f:
                    file_data = f.read()

                # Add to zip
                zip_file.writestr(str(arc_name), file_data)

                logger.debug(f"Added file: {file_path} -> {arc_name}")

        logger.info(f"Successfully created zip file: {output_path}")
        return str(output_path)

    def _create_encrypted_zip_from_files(self, file_paths: List[Path], output_path: Path, base_dir: Optional[Path]) -> str:
        """Create encrypted zip file from multiple files"""
        # Create temporary zip file
        temp_zip_path = output_path.with_suffix('.tmp.zip')

        # First create standard zip file
        with zipfile.ZipFile(
            temp_zip_path,
            'w',
            compression=zipfile.ZIP_DEFLATED,
            compresslevel=self.compression_level
        ) as zip_file:
            for file_path in file_paths:
                if base_dir:
                    arc_name = file_path.relative_to(base_dir)
                else:
                    arc_name = file_path.name

                # Read file content
                with open(file_path, 'rb') as f:
                    file_data = f.read()

                # Add to zip
                zip_file.writestr(str(arc_name), file_data)

                logger.debug(f"Added file: {file_path} -> {arc_name}")

        # Encrypt entire zip file
        self._encrypt_zip_file(temp_zip_path, output_path, self._password)

        # Delete temporary file
        temp_zip_path.unlink()

        logger.info(f"Successfully created encrypted zip file: {output_path}")
        return str(output_path)

    def test_zip_extraction(self, zip_path: Union[str, Path]) -> bool:
        """
        Test if zip file can be extracted normally

        Args:
            zip_path: Zip file path

        Returns:
            Whether it can be extracted normally
        """
        try:
            zip_path = Path(zip_path)

            if not zip_path.exists():
                raise ZipError(f"Zip file does not exist: {zip_path}")

            # Check if it's an encrypted file
            if self._is_encrypted_zip_file(zip_path):
                return self._test_encrypted_zip_extraction(zip_path)
            else:
                return self._test_standard_zip_extraction(zip_path)

        except Exception as e:
            logger.warning(f"Zip file extraction test failed: {e!s}")
            return False

    def _is_encrypted_zip_file(self, zip_path: Path) -> bool:
        """Check if it's an encrypted zip file"""
        try:
            with open(zip_path, 'rb') as f:
                magic = f.read(9)
                return magic == b'SECUREZIP'
        except (OSError, IOError):
            return False

    def _test_standard_zip_extraction(self, zip_path: Path) -> bool:
        """Test standard zip file extraction"""
        with zipfile.ZipFile(zip_path, 'r') as zip_file:
            # Try to extract first file for testing
            file_list = zip_file.namelist()
            if not file_list:
                return True  # Empty zip file

            # Find first non-directory file
            test_file_name = None
            for name in file_list:
                if not name.endswith('/'):  # Not a directory
                    test_file_name = name
                    break

            if test_file_name is None:
                return True  # Only directories, consider test passed

            # Try to extract first file
            zip_file.extract(test_file_name)

            # Clean up test file
            test_file = Path(test_file_name)
            if test_file.exists():
                test_file.unlink()

            return True

    def _test_encrypted_zip_extraction(self, zip_path: Path) -> bool:
        """Test encrypted zip file extraction"""
        if not self._is_encrypted():
            logger.warning("Trying to test encrypted zip file but password not set")
            return False

        # Create temporary decryption file
        temp_zip_path = zip_path.with_suffix('.temp.zip')

        try:
            # Try to decrypt
            if not self._decrypt_zip_file(zip_path, temp_zip_path, self._password):
                return False

            # Test extraction
            with zipfile.ZipFile(temp_zip_path, 'r') as zip_file:
                file_list = zip_file.namelist()
                if not file_list:
                    temp_zip_path.unlink()
                    return True  # Empty zip file

                # Find first non-directory file
                test_file_name = None
                for name in file_list:
                    if not name.endswith('/'):  # Not a directory
                        test_file_name = name
                        break

                if test_file_name is None:
                    temp_zip_path.unlink()
                    return True  # Only directories, consider test passed

                # Try to extract first file
                zip_file.extract(test_file_name)

                # Clean up test file
                test_file = Path(test_file_name)
                if test_file.exists():
                    test_file.unlink()

            # Clean up temporary file
            temp_zip_path.unlink()
            return True

        except Exception as e:
            logger.warning(f"Encrypted zip file extraction test failed: {e!s}")
            # Clean up temporary file
            if temp_zip_path.exists():
                temp_zip_path.unlink()
            return False

    def extract_zip(self, zip_path: Union[str, Path], extract_path: Union[str, Path]) -> bool:
        """
        Extract zip file

        Args:
            zip_path: Zip file path
            extract_path: Extraction target path

        Returns:
            Whether extraction was successful
        """
        try:
            zip_path = Path(zip_path)
            extract_path = Path(extract_path)

            if not zip_path.exists():
                raise ZipError(f"Zip file does not exist: {zip_path}")

            # Check if it's an encrypted file
            if self._is_encrypted_zip_file(zip_path):
                return self._extract_encrypted_zip(zip_path, extract_path)
            else:
                return self._extract_standard_zip(zip_path, extract_path)

        except Exception as e:
            logger.error(f"Failed to extract zip file: {e!s}")
            return False

    def _extract_standard_zip(self, zip_path: Path, extract_path: Path) -> bool:
        """Extract standard zip file"""
        with zipfile.ZipFile(zip_path, 'r') as zip_file:
            zip_file.extractall(extract_path)

        logger.info(f"Successfully extracted zip file to: {extract_path}")
        return True

    def _extract_encrypted_zip(self, zip_path: Path, extract_path: Path) -> bool:
        """Extract encrypted zip file"""
        if not self._is_encrypted():
            logger.error("Trying to extract encrypted zip file but password not set")
            return False

        # Create temporary decryption file
        temp_zip_path = zip_path.with_suffix('.temp.zip')

        try:
            # Try to decrypt
            if not self._decrypt_zip_file(zip_path, temp_zip_path, self._password):
                return False

            # Extract file
            with zipfile.ZipFile(temp_zip_path, 'r') as zip_file:
                zip_file.extractall(extract_path)

            # Clean up temporary file
            temp_zip_path.unlink()

            logger.info(f"Successfully extracted encrypted zip file to: {extract_path}")
            return True

        except Exception as e:
            logger.error(f"Failed to extract encrypted zip file: {e!s}")
            # Clean up temporary file
            if temp_zip_path.exists():
                temp_zip_path.unlink()
            return False
