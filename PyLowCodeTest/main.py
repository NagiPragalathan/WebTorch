"""
LCTP - Low-Code Testing Platform

LCTP is a Selenium-based Low-Code Web Testing Automation tool in Python. It simplifies web testing using JSON configuration files, making it easy for testers and developers to automate test scenarios.

**Note**: LCTP is a powerful tool designed to streamline your testing efforts, and we're constantly improving it. However, please note that it's still a work in progress and not ready for production use.

This module provides a command-line interface for various tasks related to the LCTP application. You can use this CLI to run tests, generate requirements files, format Python files, and perform extra functions.

Usage:
    -h, --help: Show this help message.
    --version, --V, --v: Show version information.
    -test <test_file>: Run tests based on a JSON configuration file.
    -req <requirements_file>: Create a requirements.txt file.
    -f <python_file>: Format a single Python file.
    -fa <directory>: Format all Python files in a directory.
    -extra: Run an extra function.

For more details on each option, use '-h' or '--help'.

Author: NagiPragalathan
Version: 0.0.1
"""


# Import statements
from Designer.BackGroundColor import *
from Designer.ForeGroundColor import *
import sys
from .testing import Make_test
from .modules_data import create_req, format_python_file, format_all_python_files_in_directory
import os


def print_version():
    """Prints the version information."""
    print("-" * 50)
    print(f"Version: {cyan('0.0.1')}")
    print("-" * 50)


def print_help():
    """Prints the help message with different colors."""
    print(cyan("Usage:"))
    print("-h, --help: Show this help message.")
    print(yellow("--version, --V, --v:") + " Show version information.")
    print(cyan("-test <test_file>:") + " Run tests based on a JSON configuration file.")
    print(cyan("-req <requirements_file>:") + " Create a requirements.txt file.")
    print(cyan("-f <python_file>:") + " Format a single Python file.")
    print(cyan("-fa <directory>:") + " Format all Python files in a directory.")
    print(cyan("-extra:") + " Run an extra function.")
    print()


def extra_function():
    """An example of an extra function."""
    print(cyan("Running the extra function."))
    # Add your extra functionality here.


def main():
    # Check for command-line arguments
    if len(sys.argv) == 1 or "-h" in sys.argv or "--help" in sys.argv:
        print_help()
    elif "--version" in sys.argv or "--V" in sys.argv or "--v" in sys.argv:
        print_version()
    elif "-test" in sys.argv:
        if len(sys.argv) > 2:
            Make_test(sys.argv[2])
        else:
            print(red("Error: Missing test file argument. Usage: -test <test_file>"))
    elif "-req" in sys.argv or "--req" in sys.argv or '-requirements' in sys.argv or '-r' in sys.argv:
        if len(sys.argv) > 2:
            create_req(sys.argv[2])
        else:
            print(red("Error: Missing requirements file argument. Usage: -req <requirements_file>"))
    elif "-f" in sys.argv or "-format" in sys.argv or "--f" in sys.argv or "--format" in sys.argv:
        if len(sys.argv) > 2:
            format_python_file(sys.argv[2])
        else:
            print(red("Error: Missing Python file argument. Usage: -f <python_file>"))
    elif "-fa" in sys.argv or "-formatall" in sys.argv or "--fa" in sys.argv or "--formatall" in sys.argv:
        if len(sys.argv) > 2:
            format_all_python_files_in_directory(sys.argv[2])
        else:
            print(red("Error: Missing directory argument. Usage: -fa <directory>"))
    elif "-extra" in sys.argv:
        extra_function()
    else:
        print(red("Error: Unknown command. Use -h or --help for help."))


if __name__ == "__main__":
    main()
