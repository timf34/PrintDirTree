import os
import fnmatch
import argparse
import json
import pyperclip
import io 
import sys 
from typing import List, Set, Dict

# Default preferences
DEFAULT_PREFS: Dict[str, Set[str]] = {
    "EXCLUDE_DIRS": {'venv', 'env', 'node_modules', 'dist', '.idea', '.expo', '.git', '__pycache__'},
    "EXCLUDE_FILES": {"LICENSE"}
}

PREFS_FILE: str = "../dir_tree_prefs.json"


def view_exclusions(prefs: Dict[str, Set[str]]) -> None:
    """
    Display the current excluded directories and files.
    """
    print("Currently excluded directories:")
    for d in sorted(prefs["EXCLUDE_DIRS"]):
        print(f"  - {d}")
    print("\nCurrently excluded files:")
    for f in sorted(prefs["EXCLUDE_FILES"]):
        print(f"  - {f}")


def include_back_preferences(args: argparse.Namespace, prefs: Dict[str, Set[str]]) -> None:
    """
    Include directories or files back into the directory tree.
    """
    if args.include_dir:
        prefs["EXCLUDE_DIRS"].difference_update(args.include_dir)
    if args.include_file:
        prefs["EXCLUDE_FILES"].difference_update(args.include_file)
    if args.save:
        save_preferences(prefs)


def load_preferences() -> Dict[str, Set[str]]:
    """
    Load preferences from a JSON file, converting lists back to sets.
    """
    try:
        if os.path.exists(PREFS_FILE):
            with open(PREFS_FILE, "r") as file:
                loaded_prefs = json.load(file)
                return {key: set(value) for key, value in loaded_prefs.items()}
    except json.JSONDecodeError as e:
        print(f"Error loading preferences: {e}. Using default preferences.")
    return DEFAULT_PREFS


def save_preferences(prefs: Dict[str, Set[str]]) -> None:
    """
    Save preferences to a JSON file, converting sets to lists for JSON serialization.
    """
    try:
        serializable_prefs = {key: list(value) for key, value in prefs.items()}
        with open(PREFS_FILE, "w") as file:
            json.dump(serializable_prefs, file, indent=4)
    except IOError as e:
        print(f"Error saving preferences: {e}. Changes might not be saved.")


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


def print_dir_structure(dir_path: str, exclude_dirs: Set[str], exclude_files: Set[str], prefix: str = '', dirs_only: bool = False) -> str:
    output = io.StringIO()
    
    def print_to_string(*args, **kwargs):
        print(*args, file=output, **kwargs)
    
    items: List[str] = os.listdir(dir_path)
    filtered_items: List[str] = [item for item in items if
                                 item not in exclude_dirs and not file_should_be_excluded(item, exclude_files)]
    filtered_items.sort()

    if dirs_only:
        filtered_items = [item for item in filtered_items if os.path.isdir(os.path.join(dir_path, item))]

    for i, item in enumerate(filtered_items, start=1):
        item_path: str = os.path.join(dir_path, item)
        if os.path.isdir(item_path):
            branch_char: str = '└── ' if i == len(filtered_items) else '├── '
            print_to_string(f"{prefix}{branch_char}{item}")
            next_prefix: str = f"{prefix}{'    ' if i == len(filtered_items) else '│   '}"
            print_to_string(print_dir_structure(item_path, exclude_dirs, exclude_files, next_prefix, dirs_only), end='')
        elif not dirs_only:
            branch_char: str = '└── ' if i == len(filtered_items) else '├── '
            print_to_string(f"{prefix}{branch_char}{item}")
    
    return output.getvalue()


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
    parser.add_argument('--view-exclusions', action='store_true',
                        help='View the current excluded directories and files.')
    parser.add_argument('--include-dir', type=str, nargs='*',
                        help='Directories to include back into the printout.')
    parser.add_argument('--include-file', type=str, nargs='*',
                        help='Files or file patterns to include back into the printout.')
    parser.add_argument('--dirs-only', action='store_true', help='Print only directories, excluding files')
    parser.add_argument('-c', '--copy-to-clipboard', action='store_true', help='Copy the output to clipboard')

    args = parser.parse_args()

    if args.view_exclusions:
        view_exclusions(prefs)
        return

    update_and_optionally_save_preferences(args, prefs)
    include_back_preferences(args, prefs)  # Include specified items back

    dir_path = args.dir
    if not os.path.isdir(dir_path):
        print(f"The specified directory does not exist: {dir_path}")
        return

    root_dir = os.path.basename(dir_path)
    output = f"{root_dir}\n"
    output += print_dir_structure(dir_path, set(prefs["EXCLUDE_DIRS"]), set(prefs["EXCLUDE_FILES"]), dirs_only=args.dirs_only)

    if args.copy_to_clipboard:
        pyperclip.copy(output)
        print("Directory structure has been copied to clipboard.")
    
    print(output)


if __name__ == '__main__':
    main()
