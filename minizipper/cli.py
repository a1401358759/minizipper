"""
MiniZipper Command Line Tool

Provides command line interface for creating zip files, supporting both standard zip and encrypted zip.
"""

import argparse
import sys
from pathlib import Path

from minizipper.secure_zipper import EncryptionAlgorithm, SecureZipper, ZipError


def main():
    """Main function"""
    parser = argparse.ArgumentParser(
        description='Create zip files (supports standard zip and encrypted zip)',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s -s /path/to/file.txt -o output.zip
  %(prog)s -s /path/to/directory -o output.zip --include-hidden
  %(prog)s -f file1.txt file2.txt -o output.zip
  %(prog)s -f file1.txt file2.txt -o output.zip --base-dir /path/to/base
  %(prog)s -s /path/to/file.txt -o encrypted.zip --password mypassword123
  %(prog)s -f file1.txt file2.txt -o encrypted.zip --password mypassword123
  %(prog)s -s /path/to/file.txt -o encrypted.zip --password mypassword123 --algorithm hmac_sha256
        """
    )

    # Input options (mutually exclusive)
    input_group = parser.add_mutually_exclusive_group(required=False)
    input_group.add_argument(
        '-s', '--source',
        help='Path to file or directory to compress'
    )

    input_group.add_argument(
        '-f', '--files',
        nargs='+',
        help='Multiple file paths to compress'
    )

    # Output options
    parser.add_argument(
        '-o', '--output',
        required=False,
        help='Output zip file path'
    )

    # Encryption options
    parser.add_argument(
        '--password',
        help='Encryption password (if provided, creates encrypted zip file)'
    )

    parser.add_argument(
        '--algorithm',
        choices=[alg.value for alg in EncryptionAlgorithm],
        default=EncryptionAlgorithm.XOR.value,
        help=f'Encryption algorithm (default: {EncryptionAlgorithm.XOR.value})'
    )

    # Other options
    parser.add_argument(
        '--include-hidden',
        action='store_true',
        help='Include hidden files (files starting with .)'
    )

    parser.add_argument(
        '--compression-level',
        type=int,
        choices=range(0, 10),
        default=6,
        help='Compression level (0-9, default: 6)'
    )

    parser.add_argument(
        '--base-dir',
        help='Base directory for calculating relative paths (only effective when using -f option)'
    )

    parser.add_argument(
        '--test',
        action='store_true',
        help='Test if zip file can be extracted normally after creation'
    )

    parser.add_argument(
        '--extract',
        help='Extract zip file to specified directory'
    )

    parser.add_argument(
        '--list-algorithms',
        action='store_true',
        help='List all available encryption algorithms'
    )

    parser.add_argument(
        '-v', '--verbose',
        action='store_true',
        help='Show detailed output'
    )

    args = parser.parse_args()

    # List algorithms
    if args.list_algorithms:
        print("Available encryption algorithms:")
        for alg in EncryptionAlgorithm:
            print(f"  {alg.value}: {alg.name}")
        return

    # Check required parameters
    if not args.list_algorithms:
        if not args.source and not args.files:
            parser.error("Need to specify source file or directory (-s) or file list (-f)")
        if not args.output and not args.extract:
            parser.error("Need to specify output file (-o) or extraction directory (--extract)")

    try:
        # Create SecureZipper instance
        zipper = SecureZipper(compression_level=args.compression_level)

        # Set password and algorithm (if provided)
        if args.password:
            algorithm = EncryptionAlgorithm(args.algorithm)
            zipper.setpassword(args.password, algorithm)
            print(f"🔐 Encryption mode enabled, using algorithm: {algorithm.value}")

        # Handle extraction operation
        if args.extract:
            if not args.output:
                print("❌ Extraction operation requires zip file path (-o)", file=sys.stderr)
                sys.exit(1)

            print(f"📦 Extracting file: {args.output} -> {args.extract}")
            if zipper.extract_zip(args.output, args.extract):
                print("✅ Extraction successful")
            else:
                print("❌ Extraction failed")
                sys.exit(1)
            return

        # Create zip file based on input type
        if args.source:
            # Compress single file or directory
            output_path = zipper.create_zip(
                source_path=args.source,
                output_path=args.output,
                include_hidden=args.include_hidden
            )
        else:
            # Compress multiple files
            output_path = zipper.create_zip_from_files(
                file_paths=args.files,
                output_path=args.output,
                base_dir=args.base_dir
            )

        # Display creation result
        if args.password:
            print(f"✅ Successfully created encrypted zip file: {output_path}")
        else:
            print(f"✅ Successfully created zip file: {output_path}")

        # Test extraction (if specified)
        if args.test:
            print("🔍 Testing zip file extraction...")
            if zipper.test_zip_extraction(output_path):
                print("✅ Zip file extraction test passed")
            else:
                print("❌ Zip file extraction test failed")
                sys.exit(1)

        # Display file information
        if args.verbose:
            zip_path = Path(output_path)
            if zip_path.exists():
                size_mb = zip_path.stat().st_size / (1024 * 1024)
                print(f"📁 File size: {size_mb:.2f} MB")

    except ZipError as e:
        print(f"❌ Error: {e}", file=sys.stderr)
        sys.exit(1)
    except KeyboardInterrupt:
        print("\n⚠️  Operation interrupted by user", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"❌ Unknown error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == '__main__':
    main()
