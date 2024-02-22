import os
import fnmatch
import argparse
from typing import List, Set

# Directories to exclude from the listing
EXCLUDE_DIRS: Set[str] = {'venv', 'node_modules', 'dist', '.idea', '.git', '__pycache__'}

# Files to exclude from the listing. Can include exact names or patterns
EXCLUDE_FILES: Set[str] = {"LICENSE", "*.jpg"}


def file_should_be_excluded(file_name: str) -> bool:
    """
    Checks if a file matches any of the patterns for exclusion (i.e. full file name or pattern).
    """
    return any(fnmatch.fnmatch(file_name, pattern) for pattern in EXCLUDE_FILES)


def print_dir_structure(dir_path: str, prefix: str = '') -> None:
    """
    Prints the directory structure for the given path, excluding specified directories and files.
    """
    items: List[str] = os.listdir(dir_path)
    filtered_items: List[str] = [item for item in items if
                                 item not in EXCLUDE_DIRS and not file_should_be_excluded(item)]
    filtered_items.sort()

    for i, item in enumerate(filtered_items, start=1):
        item_path: str = os.path.join(dir_path, item)
        if os.path.isdir(item_path):
            branch_char: str = '└── ' if i == len(filtered_items) else '├── '
            print(f"{prefix}{branch_char}{item}")
            next_prefix: str = f"{prefix}{'    ' if i == len(filtered_items) else '│   '}"
            print_dir_structure(item_path, next_prefix)
        else:
            branch_char: str = '└── ' if i == len(filtered_items) else '├── '
            print(f"{prefix}{branch_char}{item}")


def main() -> None:
    """
    Main function to handle argument parsing and initiate directory structure printing.
    """
    parser: argparse.ArgumentParser = argparse.ArgumentParser(description='Print the directory tree structure.')
    parser.add_argument('--dir', type=str, default=os.getcwd(),
                        help='The directory path to print the structure of. Defaults to the current directory.')

    args: argparse.Namespace = parser.parse_args()

    dir_path: str = args.dir
    if not os.path.isdir(dir_path):
        print(f"The specified directory does not exist: {dir_path}")
        return

    print(os.path.basename(dir_path))
    print_dir_structure(dir_path)


if __name__ == '__main__':
    main()
