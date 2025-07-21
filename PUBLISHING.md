# Publishing MiniZipper to PyPI

This document explains how to publish the MiniZipper package to PyPI.

## Prerequisites

1. **PyPI Account**: Create an account on [PyPI](https://pypi.org/account/register/)
2. **TestPyPI Account**: Create an account on [TestPyPI](https://test.pypi.org/account/register/)
3. **API Tokens**: Generate API tokens for both PyPI and TestPyPI

## Setup API Tokens

### PyPI API Token
1. Go to [PyPI Account Settings](https://pypi.org/manage/account/)
2. Click "Add API token"
3. Give it a name (e.g., "minizipper-publish")
4. Select "Entire account (all projects)"
5. Copy the token (it starts with `pypi-`)

### TestPyPI API Token
1. Go to [TestPyPI Account Settings](https://test.pypi.org/manage/account/)
2. Click "Add API token"
3. Give it a name (e.g., "minizipper-test-publish")
4. Select "Entire account (all projects)"
5. Copy the token (it starts with `pypi-`)

## GitHub Secrets Setup

For automatic publishing via GitHub Actions, add these secrets to your repository:

1. Go to your GitHub repository
2. Click "Settings" → "Secrets and variables" → "Actions"
3. Add the following secrets:
   - `PYPI_API_TOKEN`: Your PyPI API token
   - `TEST_PYPI_API_TOKEN`: Your TestPyPI API token

## Publishing Methods

### Method 1: GitHub Actions (Recommended)

1. **Create a Release**:
   - Go to your GitHub repository
   - Click "Releases" → "Create a new release"
   - Tag version: `v0.0.1` (must match your package version)
   - Title: `MiniZipper v0.0.1`
   - Description: Add release notes
   - Check "Set as the latest release"
   - Click "Publish release"

2. **Automatic Publishing**:
   - The GitHub Actions workflow will automatically trigger
   - Package will be built and published to PyPI
   - Check the Actions tab for progress

### Method 2: Manual Publishing

1. **Build the package**:
   ```bash
   # Clean previous builds
   rm -rf build/ dist/ *.egg-info/

   # Install build tools
   python -m pip install --upgrade build twine

   # Build package
   python -m build
   ```

2. **Check the package**:
   ```bash
   python -m twine check dist/*
   ```

3. **Publish to TestPyPI (for testing)**:
   ```bash
   python -m twine upload --repository testpypi dist/*
   ```

4. **Publish to PyPI**:
   ```bash
   python -m twine upload dist/*
   ```

### Method 3: Using the Publish Script

1. **Run the script**:
   ```bash
   ./scripts/publish.sh
   ```

2. **Follow the prompts** to choose publishing destination

## Version Management

### Updating Version

1. **Update version in code**:
   ```python
   # In minizipper/__init__.py
   __version__ = "0.0.2"  # Increment version
   ```

2. **Update setup.py** (if needed):
   ```python
   # In setup.py
   version = "0.0.2"  # Should match __init__.py
   ```

3. **Create new release** with matching tag

### Version Numbering

- `0.0.x`: Development releases
- `0.x.0`: Beta releases
- `1.0.0`: First stable release
- `x.y.z`: Major.Minor.Patch

## Testing Before Publishing

### Local Testing
```bash
# Install in development mode
pip install -e .

# Run tests
pytest minizipper/tests/

# Test CLI
python -m minizipper.cli --help
```

### TestPyPI Testing
```bash
# Install from TestPyPI
pip install --index-url https://test.pypi.org/simple/ minizipper

# Test functionality
python -c "from minizipper import SecureZipper; print('Success!')"
```

## Troubleshooting

### Common Issues

1. **Package name already exists**:
   - Check if the name is available on PyPI
   - Consider using a different name or adding a prefix

2. **Authentication failed**:
   - Verify your API tokens are correct
   - Check if tokens have the right permissions

3. **Build errors**:
   - Ensure all dependencies are listed in `setup.py`
   - Check for syntax errors in your code

4. **Version conflicts**:
   - PyPI doesn't allow re-uploading the same version
   - Increment version number before re-publishing

### Getting Help

- [PyPI Help](https://pypi.org/help/)
- [Python Packaging User Guide](https://packaging.python.org/)
- [Twine Documentation](https://twine.readthedocs.io/)

## Security Notes

- Never commit API tokens to version control
- Use GitHub Secrets for CI/CD
- Regularly rotate your API tokens
- Test on TestPyPI before publishing to PyPI
