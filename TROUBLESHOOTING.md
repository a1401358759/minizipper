# Troubleshooting Guide

This document helps you resolve common issues with MiniZipper development and publishing.

## PyPI Publishing Issues

### Error: "Username/Password authentication is no longer supported"

**Problem**: PyPI no longer accepts username/password authentication.

**Solution**: Use API tokens instead.

#### Step 1: Get PyPI API Token

1. Go to [PyPI Account Settings](https://pypi.org/manage/account/)
2. Click "Add API token"
3. Give it a name (e.g., "minizipper-publish")
4. Select "Entire account (all projects)"
5. Copy the token (it starts with `pypi-`)

#### Step 2: Set GitHub Secrets

1. Go to your GitHub repository
2. Click "Settings" → "Secrets and variables" → "Actions"
3. Add new secret:
   - Name: `PYPI_API_TOKEN`
   - Value: Your PyPI API token (starts with `pypi-`)

#### Step 3: Verify Configuration

Run the authentication test script:

```bash
# Set your token locally for testing
export PYPI_API_TOKEN='pypi-your-token-here'

# Run the test script
python scripts/test_pypi_auth.py
```

### Error: "403 Forbidden"

**Problem**: Authentication failed.

**Possible Causes**:
1. API token is incorrect or expired
2. Token doesn't have upload permissions
3. Token format is wrong

**Solutions**:

1. **Check token format**:
   ```bash
   # Token should start with 'pypi-'
   echo $PYPI_API_TOKEN | head -c 10
   # Should output: pypi-
   ```

2. **Regenerate token**:
   - Go to PyPI account settings
   - Delete old token
   - Create new token
   - Update GitHub Secrets

3. **Check token permissions**:
   - Ensure token has "Entire account (all projects)" scope
   - Or create project-specific token for "minizipper"

### Error: "Package name already exists"

**Problem**: The package name is already taken on PyPI.

**Solutions**:
1. Choose a different package name
2. Add a prefix/suffix to make it unique
3. Contact the existing package owner

## GitHub Actions Issues

### Workflow not triggering

**Check**:
1. Release tag matches version in code
2. Release is published (not draft)
3. Workflow file is in `.github/workflows/`

### Build failures

**Common causes**:
1. Python version compatibility
2. Missing dependencies
3. Syntax errors

**Debug**:
1. Check Actions tab for detailed logs
2. Run tests locally first
3. Check Python version compatibility

## Local Development Issues

### Import errors

**Problem**: `ModuleNotFoundError: No module named 'minizipper'`

**Solutions**:
```bash
# Install in development mode
pip install -e .

# Or add to PYTHONPATH
export PYTHONPATH="${PYTHONPATH}:$(pwd)"
```

### Test failures

**Problem**: Tests are failing locally.

**Solutions**:
1. Install development dependencies:
   ```bash
   pip install -r requirements-dev.txt
   ```

2. Run tests with verbose output:
   ```bash
   pytest minizipper/tests/ -v
   ```

3. Check Python version compatibility:
   ```bash
   python --version
   # Should be 3.8 or higher
   ```

## Package Building Issues

### Build errors

**Problem**: `python -m build` fails.

**Solutions**:
1. Clean previous builds:
   ```bash
   rm -rf build/ dist/ *.egg-info/
   ```

2. Install build tools:
   ```bash
   pip install --upgrade build twine
   ```

3. Check setup.py syntax:
   ```bash
   python setup.py check
   ```

### Package validation errors

**Problem**: `twine check` fails.

**Solutions**:
1. Check package metadata in setup.py
2. Verify README.md exists and is valid
3. Check for syntax errors in Python files

## Getting Help

### Useful Resources

- [PyPI Help](https://pypi.org/help/)
- [Python Packaging User Guide](https://packaging.python.org/)
- [Twine Documentation](https://twine.readthedocs.io/)
- [GitHub Actions Documentation](https://docs.github.com/en/actions)

### Debug Commands

```bash
# Test PyPI authentication
python scripts/test_pypi_auth.py

# Check package locally
python -m build
python -m twine check dist/*

# Test installation
pip install dist/*.whl

# Run all tests
pytest minizipper/tests/ -v --cov=minizipper
```

### Common Environment Variables

```bash
# For local testing
export PYPI_API_TOKEN='pypi-your-token-here'
export TWINE_USERNAME='__token__'
export TWINE_PASSWORD='pypi-your-token-here'

# For development
export PYTHONPATH="${PYTHONPATH}:$(pwd)"
```
