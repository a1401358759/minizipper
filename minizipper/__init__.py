"""
MiniZipper - Create zip files, supporting standard zip and password-encrypted zip

This package provides functionality to create zip files, supporting both standard zip and password-encrypted zip,
ensuring that generated zip files can be extracted normally on Windows, macOS, Linux and other platforms.
Supports multiple encryption algorithm choices.
"""

from .secure_zipper import EncryptionAlgorithm, SecureZipper, ZipError

__version__ = "0.0.2"
__author__ = "yxuefeng"
__email__ = "a1401358759@outlook.com"

__all__ = ["EncryptionAlgorithm", "SecureZipper", "ZipError"]
