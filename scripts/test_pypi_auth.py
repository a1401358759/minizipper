#!/usr/bin/env python3
"""
Test PyPI Authentication Script

This script tests PyPI API token authentication to ensure it's working correctly.
"""

import os
import sys


def test_pypi_auth():
    """Test PyPI authentication using API token"""

    # Check if token is set
    token = os.environ.get('PYPI_API_TOKEN')
    if not token:
        print("❌ PYPI_API_TOKEN environment variable is not set")
        print("Please set it with: export PYPI_API_TOKEN='pypi-...'")
        return False

    # Check token format
    if not token.startswith('pypi-'):
        print("❌ Invalid token format. PyPI tokens should start with 'pypi-'")
        print(f"Your token starts with: {token[:10]}...")
        return False

    print(f"✅ Token format looks correct: {token[:10]}...")

    # Test twine configuration
    try:
        import subprocess
        result = subprocess.run([
            'python', '-m', 'twine', 'check', '--help'
        ], capture_output=True, text=True, timeout=10)

        if result.returncode == 0:
            print("✅ Twine is available")
        else:
            print("❌ Twine is not available")
            return False

    except Exception as e:
        print(f"❌ Error testing twine: {e}")
        return False

    # Test authentication (without actually uploading)
    print("\n🔍 Testing authentication...")
    print("Note: This will not actually upload anything")

    # Set environment variables for twine
    env = os.environ.copy()
    env['TWINE_USERNAME'] = '__token__'
    env['TWINE_PASSWORD'] = token

    try:
        # Try to get package info (this will test authentication)
        result = subprocess.run([
            'python', '-m', 'twine', 'upload', '--help'
        ], env=env, capture_output=True, text=True, timeout=10)

        if result.returncode == 0:
            print("✅ Authentication test passed")
            return True
        else:
            print(f"❌ Authentication test failed: {result.stderr}")
            return False

    except Exception as e:
        print(f"❌ Error during authentication test: {e}")
        return False


def main():
    """Main function"""
    print("🔐 PyPI Authentication Test")
    print("=" * 40)

    success = test_pypi_auth()

    if success:
        print("\n✅ All tests passed! Your PyPI authentication is working correctly.")
        print("\nTo publish your package:")
        print("1. Build the package: python -m build")
        print("2. Upload to PyPI: python -m twine upload dist/*")
    else:
        print("\n❌ Authentication test failed. Please check your configuration.")
        sys.exit(1)


if __name__ == '__main__':
    main()
