import os
import fnmatch
import argparse
import json
from typing import List, Set, Dict

# Default preferences
DEFAULT_PREFS: Dict[str, Set[str]] = {
    "EXCLUDE_DIRS": {'venv', 'env', 'node_modules', 'dist', '.idea', '.git', '__pycache__'},
    "EXCLUDE_FILES": {"LICENSE", "*.jpg"}
}

PREFS_FILE: str = "dir_tree_prefs.json"


def load_preferences() -> Dict[str, Set[str]]:
    """
    Load preferences from a JSON file, converting lists back to sets.
    """
    if os.path.exists(PREFS_FILE):
        with open(PREFS_FILE, "r") as file:
            loaded_prefs = json.load(file)
            return {key: set(value) for key, value in loaded_prefs.items()}
    return DEFAULT_PREFS


def save_preferences(prefs: Dict[str, Set[str]]) -> None:
    """
    Save preferences to a JSON file, converting sets to lists for JSON serialization.
    """
    serializable_prefs = {key: list(value) for key, value in prefs.items()}
    with open(PREFS_FILE, "w") as file:
        json.dump(serializable_prefs, file, indent=4)


def update_and_optionally_save_preferences(args: argparse.Namespace, prefs: Dict[str, Set[str]]) -> None:
    """
    Update preferences based on command-line arguments and optionally save them.
    """
    if args.exclude_dir:
        prefs["EXCLUDE_DIRS"].update(args.exclude_dir)
    if args.exclude_file:
        prefs["EXCLUDE_FILES"].update(args.exclude_file)
    if args.save:
        save_preferences(prefs)


def file_should_be_excluded(file_name: str, exclude_files: Set[str]) -> bool:
    """
    Check if a file matches any of the patterns for exclusion.
    """
    return any(fnmatch.fnmatch(file_name, pattern) for pattern in exclude_files)


def print_dir_structure(dir_path: str, exclude_dirs: Set[str], exclude_files: Set[str], prefix: str = '') -> None:
    """
    Print the directory structure for the given path, excluding specified directories and files.
    """
    items: List[str] = os.listdir(dir_path)
    filtered_items: List[str] = [item for item in items if
                                 item not in exclude_dirs and not file_should_be_excluded(item, exclude_files)]
    filtered_items.sort()

    for i, item in enumerate(filtered_items, start=1):
        item_path: str = os.path.join(dir_path, item)
        if os.path.isdir(item_path):
            branch_char: str = '└── ' if i == len(filtered_items) else '├── '
            print(f"{prefix}{branch_char}{item}")
            next_prefix: str = f"{prefix}{'    ' if i == len(filtered_items) else '│   '}"
            print_dir_structure(item_path, exclude_dirs, exclude_files, next_prefix)
        else:
            branch_char: str = '└── ' if i == len(filtered_items) else '├── '
            print(f"{prefix}{branch_char}{item}")


def main() -> None:
    """
    Main function to handle argument parsing and initiate directory structure printing.
    """
    prefs = load_preferences()

    parser = argparse.ArgumentParser(description='Print the directory tree structure with customizable exclusions.')
    parser.add_argument('--dir', type=str, default=os.getcwd(),
                        help='The directory path to print the structure of. Defaults to the current directory.')
    parser.add_argument('--exclude-dir', type=str, nargs='*', help='Directories to exclude from the printout.')
    parser.add_argument('--exclude-file', type=str, nargs='*',
                        help='Files or file patterns to exclude from the printout.')
    parser.add_argument('--save', action='store_true', help='Save the specified exclusions for future runs.')

    args = parser.parse_args()

    update_and_optionally_save_preferences(args, prefs)

    dir_path = args.dir
    if not os.path.isdir(dir_path):
        print(f"The specified directory does not exist: {dir_path}")
        return

    print(os.path.basename(dir_path))
    print_dir_structure(dir_path, set(prefs["EXCLUDE_DIRS"]), set(prefs["EXCLUDE_FILES"]))


if __name__ == '__main__':
    main()
