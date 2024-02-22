import os

# Directories to exclude from the listing
EXCLUDE_DIRS = {'venv', 'node_modules', 'dist', '.idea', '.git', '__pycache__'}

EXCLUDE_FILES = {"LICENSE", "*.jpg"}

def print_dir_structure(dir_path, prefix=''):
    """
    Prints the directory structure for the given path in a Markdown-like format, excluding specified directories.

    :param dir_path: The root directory path to print the structure of.
    :param prefix: The prefix to use before printing (used for recursive calls to indicate depth).
    """
    # Print the name of the directory
    # print(f"{os.path.basename(dir_path)}")

    items = [item for item in os.listdir(dir_path) if item not in EXCLUDE_DIRS]
    items.sort()  # Optional: sort items to keep the directory listing consistent
    for i, item in enumerate(items, start=1):
        item_path = os.path.join(dir_path, item)
        if os.path.isdir(item_path):
            # Determine whether to use the "last item" branch character or "not last" pipe character
            print(f"{prefix}{'└── ' if i == len(items) else '├── '}{item}")
            # Recurse into directories, adjusting the prefix depending on item order
            next_prefix = f"{prefix}{'    ' if i == len(items) else '│   '}"
            print_dir_structure(item_path, next_prefix)
        else:
            # It's a file; determine how to print based on item order
            print(f"{prefix}{'└── ' if i == len(items) else '├── '}{item}")


if __name__ == '__main__':
    # Start from the current directory or specify any directory you want to scan
    # start_path = r'C:\Users\timf3\PycharmProjects\PrintDirectory'
    start_path = r'C:\Users\timf3\WebstormProjects\mona_lisa_eyes'

    # Print the name of the root directory
    print(os.path.basename(start_path))

    print_dir_structure(start_path)
