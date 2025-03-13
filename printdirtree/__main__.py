import os
import fnmatch
import argparse
import json
import pyperclip
import io 
import sys 
from typing import List, Set, Dict, Tuple

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


def path_should_be_excluded(rel_path: str, exclude_dirs: Set[str]) -> bool:
    """
    Check if a path or any of its parent directories should be excluded.
    This handles both direct matches and path pattern matches.
    """
    # Check for direct match of the full relative path
    if rel_path in exclude_dirs:
        return True

    # Check if path matches any exclusion patterns
    for pattern in exclude_dirs:
        # Handle path patterns (with slashes)
        if '/' in pattern and fnmatch.fnmatch(rel_path, pattern):
            return True

        # Handle directory name patterns (just the basename)
        path_parts = rel_path.split(os.sep)
        if any(fnmatch.fnmatch(part, pattern) for part in path_parts):
            return True

    return False


def read_file_contents(file_path: str) -> str:
    """
    Read and return the contents of a file, handling potential errors.
    """
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            return f.read().strip()
    except UnicodeDecodeError:
        return "[Binary file]"
    except Exception as e:
        return f"[Error reading file: {str(e)}]"


def print_dir_structure(
        dir_path: str,
        exclude_dirs: Set[str],
        exclude_files: Set[str],
        prefix: str = '',
        dirs_only: bool = False,
        show_contents: bool = False,
        root_path: str = None,
        current_rel_path: str = ''
) -> Tuple[str, List[Tuple[str, str]]]:
    """
    Print directory structure and optionally collect file contents.
    Returns a tuple of (tree_structure, list of (relative_path, content) pairs).
    """
    output = io.StringIO()
    file_contents = []

    if root_path is None:
        root_path = dir_path

    def print_to_string(*args, **kwargs):
        print(*args, file=output, **kwargs)

    items: List[str] = os.listdir(dir_path)
    filtered_items: List[str] = []

    for item in sorted(items):
        item_path = os.path.join(dir_path, item)
        item_rel_path = os.path.join(current_rel_path, item) if current_rel_path else item

        # Check if this item or its path should be excluded
        if path_should_be_excluded(item_rel_path, exclude_dirs):
            continue

        if os.path.isfile(item_path) and file_should_be_excluded(item, exclude_files):
            continue

        filtered_items.append((item, item_rel_path))

    if dirs_only:
        filtered_items = [(item, rel_path) for item, rel_path in filtered_items if
                          os.path.isdir(os.path.join(dir_path, item))]

    for i, (item, item_rel_path) in enumerate(filtered_items, start=1):
        item_path: str = os.path.join(dir_path, item)
        if os.path.isdir(item_path):
            branch_char: str = '└── ' if i == len(filtered_items) else '├── '
            print_to_string(f"{prefix}{branch_char}{item}")
            next_prefix: str = f"{prefix}{'    ' if i == len(filtered_items) else '│   '}"
            subtree, subcontents = print_dir_structure(
                item_path, exclude_dirs, exclude_files, next_prefix,
                dirs_only, show_contents, root_path, item_rel_path
            )
            print_to_string(subtree, end='')
            file_contents.extend(subcontents)
        elif not dirs_only:
            branch_char: str = '└── ' if i == len(filtered_items) else '├── '
            print_to_string(f"{prefix}{branch_char}{item}")

            if show_contents:
                rel_path = os.path.relpath(item_path, root_path)
                content = read_file_contents(item_path)
                file_contents.append((rel_path, content))

    return output.getvalue(), file_contents


def main() -> None:
    """
    Main function to handle argument parsing and initiate directory structure printing.
    """
    prefs = load_preferences()

    parser = argparse.ArgumentParser(description='Print the directory tree structure with customizable exclusions.')
    parser.add_argument('--dir', type=str, default=os.getcwd(),
                        help='The directory path to print the structure of. Defaults to the current directory.')
    parser.add_argument('--exclude-dir', type=str, nargs='*',
                        help='Directories or path patterns to exclude from the printout.')
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
    parser.add_argument('-p', '--show-contents', action='store_true',
                        help='Show the contents of each file after the tree structure')

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
    tree_output = f"{root_dir}\n"
    tree_structure, file_contents = print_dir_structure(
        dir_path,
        set(prefs["EXCLUDE_DIRS"]),
        set(prefs["EXCLUDE_FILES"]),
        dirs_only=args.dirs_only,
        show_contents=args.show_contents
    )

    output = tree_output + tree_structure

    if args.show_contents and file_contents:
        output += "\n"  # Add a blank line between tree and contents
        for rel_path, content in file_contents:
            output += f"\n# {rel_path}\n{content}\n"

    if args.copy_to_clipboard:
        pyperclip.copy(output)
        print("Directory structure has been copied to clipboard.")

    print(output)


if __name__ == '__main__':
    main()