"""
MiniZipper Package Installation Configuration

Used for installing and distributing the minizipper package.
"""

from pathlib import Path

from setuptools import find_packages, setup

# Read README file
readme_path = Path(__file__).parent / "README.md"
long_description = ""
if readme_path.exists():
    with open(readme_path, "r", encoding="utf-8") as f:
        long_description = f.read()

# Read version information
version_path = Path(__file__).parent / "minizipper" / "__init__.py"
version = "0.0.1"
if version_path.exists():
    with open(version_path, "r", encoding="utf-8") as f:
        for line in f:
            if line.startswith("__version__"):
                version = line.split("=")[1].strip().strip('"\'')
                break

setup(
    name="minizipper",
    version=version,
    author="yxuefeng",
    author_email="a1401358759@outlook.com",
    description="Create password-encrypted zip files, supports extraction on all platforms",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/a1401358759/minizipper",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Topic :: System :: Archiving :: Compression",
        "Topic :: Security :: Cryptography",
    ],
    python_requires=">=3.8",
    install_requires=[
        # Uses Python standard library, no external dependencies required
    ],
    extras_require={
        "dev": [
            "pytest>=7.0",
            "pytest-cov>=4.0",
            "black>=23.0",
            "flake8>=6.0",
            "mypy>=1.0",
        ],
    },
    entry_points={
        "console_scripts": [
            "minizipper=minizipper.cli:main",
        ],
    },
    keywords="zip encryption password security cross-platform",
    project_urls={
        "Bug Reports": "https://github.com/a1401358759/minizipper/issues",
        "Source": "https://github.com/a1401358759/minizipper",
        "Documentation": "https://github.com/a1401358759/minizipper#readme",
    },
)
