# MiniZipper

A Python library for creating zip files, supporting both standard zip and password-encrypted zip, ensuring that generated zip files can be extracted normally on Windows, macOS, Linux and other platforms.

## Features

- ✅ **Cross-platform compatibility**: Generated zip files can be extracted normally on all major operating systems
- ✅ **Multiple encryption algorithms**: Supports 5 different encryption algorithm choices
- ✅ **Easy to use**: Simple API, create encrypted zip with just a few lines of code
- ✅ **No external dependencies**: Uses only Python standard library, no additional packages required
- ✅ **Command line tool**: Provides convenient command line interface
- ✅ **Batch processing**: Supports single file, directory or batch file compression
- ✅ **Context manager support**: Automatic cleanup of sensitive data with `with` statements

## Supported Encryption Algorithms

| Algorithm | Identifier | Description | Security Level |
|-----------|------------|-------------|----------------|
| XOR | `xor` | Simple XOR encryption (default) | Basic |
| HMAC-SHA256 | `hmac_sha256` | HMAC-SHA256 based encryption | High |
| AES-Like | `aes_like` | AES-like multi-round encryption | Medium-High |
| Double XOR | `double_xor` | Double XOR encryption | Medium |
| Custom Hash | `custom_hash` | Multi-hash algorithm combination encryption | Medium-High |

## Installation

```bash
pip install minizipper
```

Or install from source:

```bash
git clone https://github.com/a1401358759/minizipper.git
cd minizipper
pip install -e .
```

## Quick Start

### Basic Usage

```python
from minizipper import SecureZipper, EncryptionAlgorithm

# Create zipper instance
zipper = SecureZipper()

# Create standard zip file
zipper.create_zip("my_file.txt", "output.zip")

# Create encrypted zip file (using default XOR algorithm)
zipper.setpassword("mypassword123")
zipper.create_zip("my_file.txt", "encrypted.zip")

# Use specific encryption algorithm
zipper.setpassword("mypassword123", EncryptionAlgorithm.HMAC_SHA256)
zipper.create_zip("my_file.txt", "secure.zip")
```

### Compress Directory

```python
from minizipper import SecureZipper

zipper = SecureZipper()

# Compress entire directory
zipper.create_zip("my_directory", "archive.zip")

# Include hidden files
zipper.create_zip("my_directory", "archive.zip", include_hidden=True)
```

### Batch File Compression

```python
from minizipper import SecureZipper

zipper = SecureZipper()

# Compress multiple files
files = ["file1.txt", "file2.txt", "file3.txt"]
zipper.create_zip_from_files(files, "multiple_files.zip")

# Specify base directory
zipper.create_zip_from_files(files, "multiple_files.zip", base_dir="/path/to/base")
```

### Extract Files

```python
from minizipper import SecureZipper

zipper = SecureZipper()

# Extract standard zip file
zipper.extract_zip("archive.zip", "extracted_folder")

# Extract encrypted zip file
zipper.setpassword("mypassword123")
zipper.extract_zip("encrypted.zip", "extracted_folder")
```

## Command Line Tool

### Basic Usage

```bash
# Compress single file
python -m minizipper.cli -s my_file.txt -o output.zip

# Compress directory
python -m minizipper.cli -s my_directory -o archive.zip

# Compress multiple files
python -m minizipper.cli -f file1.txt file2.txt file3.txt -o multiple.zip
```

### Encryption Features

```bash
# Use default algorithm (XOR) encryption
python -m minizipper.cli -s my_file.txt -o encrypted.zip --password mypass123

# Use specific algorithm encryption
python -m minizipper.cli -s my_file.txt -o secure.zip --password mypass123 --algorithm hmac_sha256

# View all available algorithms
python -m minizipper.cli --list-algorithms
```

### Extraction Features

```bash
# Extract standard zip file
python -m minizipper.cli -o archive.zip --extract extracted_folder

# Extract encrypted zip file
python -m minizipper.cli -o encrypted.zip --extract extracted_folder --password mypass123
```

### Advanced Options

```bash
# Include hidden files
python -m minizipper.cli -s my_directory -o archive.zip --include-hidden

# Set compression level
python -m minizipper.cli -s my_file.txt -o output.zip --compression-level 9

# Test zip file
python -m minizipper.cli -s my_file.txt -o test.zip --test

# Verbose output
python -m minizipper.cli -s my_file.txt -o output.zip -v
```

## API Reference

### SecureZipper Class

#### Constructor

```python
SecureZipper(compression_level: int = 6)
```

- `compression_level`: Compression level (0-9), default is 6

#### Context Manager Support

SecureZipper supports context managers and can be used with `with` statements:

```python
# Using context manager (recommended)
with SecureZipper() as zipper:
    zipper.setpassword("mypassword123", EncryptionAlgorithm.HMAC_SHA256)
    zipper.create_zip("source_folder", "encrypted.zip")
    # Automatic cleanup of sensitive data

# Traditional way
zipper = SecureZipper()
zipper.setpassword("mypassword123")
zipper.create_zip("source_folder", "encrypted.zip")
# Manual cleanup required
```

**Context Manager Benefits:**
- Automatic cleanup of sensitive data
- Exception handling and logging
- Cleaner, more readable code
- Resource management

#### Main Methods

##### setpassword()

```python
setpassword(password: str, algorithm: EncryptionAlgorithm = EncryptionAlgorithm.XOR)
```

Set encryption password and algorithm.

- `password`: Encryption password, if None or empty string, encryption is disabled
- `algorithm`: Encryption algorithm, default is XOR

##### create_zip()

```python
create_zip(
    source_path: Union[str, Path],
    output_path: Union[str, Path],
    include_hidden: bool = False
) -> str
```

Create zip file.

- `source_path`: Path to file or directory to compress
- `output_path`: Output zip file path
- `include_hidden`: Whether to include hidden files
- Returns: Created zip file path

##### create_zip_from_files()

```python
create_zip_from_files(
    file_paths: List[Union[str, Path]],
    output_path: Union[str, Path],
    base_dir: Optional[Union[str, Path]] = None
) -> str
```

Create zip file from multiple files.

- `file_paths`: List of file paths to compress
- `output_path`: Output zip file path
- `base_dir`: Base directory for calculating relative paths
- Returns: Created zip file path

##### extract_zip()

```python
extract_zip(
    zip_path: Union[str, Path],
    extract_path: Union[str, Path]
) -> bool
```

Extract zip file.

- `zip_path`: Zip file path
- `extract_path`: Extraction target path
- Returns: Whether extraction was successful

##### test_zip_extraction()

```python
test_zip_extraction(zip_path: Union[str, Path]) -> bool
```

Test if zip file can be extracted normally.

- `zip_path`: Zip file path
- Returns: Whether it can be extracted normally

## Encryption Algorithm Details

### 1. XOR (xor)
- **Principle**: Simple XOR operation with key
- **Features**: Fast, lightweight
- **Use cases**: Basic protection needs

### 2. HMAC-SHA256 (hmac_sha256)
- **Principle**: HMAC-SHA256 hash-based encryption
- **Features**: High security, salt-based
- **Use cases**: High security requirements

### 3. AES-Like (aes_like)
- **Principle**: Simulated AES multi-round encryption
- **Features**: Medium-high security
- **Use cases**: Balance between security and performance

### 4. Double XOR (double_xor)
- **Principle**: Two rounds of XOR encryption
- **Features**: Enhanced XOR security
- **Use cases**: Medium security requirements

### 5. Custom Hash (custom_hash)
- **Principle**: Combination of MD5, SHA1, SHA256 hash algorithms
- **Features**: Multi-hash protection
- **Use cases**: Scenarios requiring multi-layer protection

## Examples

### Example 1: Basic File Compression

```python
from minizipper import SecureZipper

# Create zipper
zipper = SecureZipper()

# Compress single file
zipper.create_zip("document.txt", "document.zip")
print("File compression completed!")
```

### Example 2: Directory Compression

```python
from minizipper import SecureZipper

zipper = SecureZipper()

# Compress entire project directory
zipper.create_zip("my_project", "project_backup.zip", include_hidden=True)
print("Project backup completed!")
```

### Example 3: Encrypted Compression

```python
from minizipper import SecureZipper, EncryptionAlgorithm

zipper = SecureZipper()

# Use HMAC-SHA256 algorithm encryption
zipper.setpassword("secure_password_123", EncryptionAlgorithm.HMAC_SHA256)
zipper.create_zip("sensitive_data", "encrypted_backup.zip")
print("Sensitive data encrypted backup completed!")
```

### Example 4: Batch File Processing

```python
from minizipper import SecureZipper

zipper = SecureZipper()

# Batch compress multiple files
files = [
    "report1.pdf",
    "report2.pdf",
    "data.csv",
    "config.json"
]

zipper.create_zip_from_files(files, "reports.zip")
print("Batch file compression completed!")
```

### Example 5: Extract and Verify

```python
from minizipper import SecureZipper

zipper = SecureZipper()

# Test zip file integrity
if zipper.test_zip_extraction("archive.zip"):
    print("Zip file is intact, starting extraction...")

    # Extract file
    if zipper.extract_zip("archive.zip", "extracted_files"):
        print("Extraction successful!")
    else:
        print("Extraction failed!")
else:
    print("Zip file is corrupted!")
```

### Example 6: Context Manager Usage

```python
from minizipper import SecureZipper, EncryptionAlgorithm

# Using context manager (recommended)
with SecureZipper() as zipper:
    zipper.setpassword("mypassword123", EncryptionAlgorithm.HMAC_SHA256)
    zipper.create_zip("source_folder", "encrypted.zip")
    # Automatic cleanup of sensitive data

print("Context manager automatically cleaned up sensitive data")
```

## Notes

1. **Password Security**: Please use strong passwords, avoid using simple passwords
2. **Algorithm Selection**: Choose appropriate encryption algorithm based on security requirements
3. **File Size**: Encryption will increase file size, especially HMAC algorithm
4. **Compatibility**: Encrypted zip files can only be extracted using this library
5. **Backup**: Please backup important files to avoid password loss

## Contributing

Welcome to submit Issues and Pull Requests!

## License

MIT License
