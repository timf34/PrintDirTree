import os

# Directories to exclude from the listing
EXCLUDE_DIRS = {'venv', 'node_modules', 'dist', '.git', '.idea', '__pycache__'}

def print_dir_structure(dir_path, indent=0):
    """
    Prints the directory structure for the given path, excluding specified directories.

    :param dir_path: The root directory path to print the structure of.
    :param indent: The indentation level (used for recursive calls to indicate depth).
    """
    # Get all items in the directory, excluding the ones in EXCLUDE_DIRS
    try:
        items = [item for item in os.listdir(dir_path) if item not in EXCLUDE_DIRS]
    except PermissionError:
        # Skip directories where permission is denied
        return

    for item in items:
        item_path = os.path.join(dir_path, item)
        if os.path.isdir(item_path):
            # It's a directory, print its name and recurse into it
            print('    ' * indent + f'[{item}]')
            print_dir_structure(item_path, indent + 1)
        else:
            # It's a file, just print its name
            print('    ' * indent + item)

if __name__ == '__main__':
    # Start from the current directory or specify any directory you want to scan
    start_path = r'C:\Users\timf3\PycharmProjects\PrintDirectory'
    # start_path = r
    print('Project Directory Structure:')
    print_dir_structure(start_path)
