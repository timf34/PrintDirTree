# PrintDirTree

`printdirtree` is a command-line utility that prints the structure of a directory tree, 
allowing you to easily specify files and directories to exclude. 

You can now also print the contents of all files, which is very useful for prompting LLMs. 

**Example:**

```bash
$ printdirtree
PrintDirTree
├── MANIFEST.in
├── README.md
├── printdirtree
│   ├── __init__.py
│   └── __main__.py
└── setup.py
```

This tool is very useful to aid with prompting ChatGPT. 

## Installation

Install `printdirtree` easily with pip:

```sh
pip install printdirtree
```

## Usage

To use `printdirtree`, simply run the command followed by optional arguments to tailor the output to your needs. 
The basic usage prints the current directory structure:

```sh
printdirtree
```

### Specifying a Directory

To print the structure of a specific directory:

```sh
printdirtree --dir /path/to/directory
```

### Excluding Directories and Files

Exclude specific directories and/or file patterns:

```sh
printdirtree --exclude-dir node_modules --exclude-dir .git --exclude-file "*.log"
```

### Saving Preferences

To save your exclusions for future runs:

```sh
printdirtree --exclude-dir temp --exclude-file "*.tmp" --save
```

### Viewing Current Exclusions

See what exclusions are currently saved:

```sh
printdirtree --view-exclusions
```

### Including Directories and Files Back

To remove exclusions and include directories or files back into the printout:

```sh
printdirtree --include-dir temp --include-file "*.tmp" --save
```

### Showing File Contents

To display both the directory structure and the contents of all files:

```sh
printdirtree --show-contents
```

This will output the directory tree followed by each file's contents with its relative path as a comment. For example:

```
temp
├── a.py
└── b.py

# temp/a.py
print("a.py")

# temp/b.py
print("b.py")
```

This is particularly useful when sharing code with LLMs, as it provides both structure and content in a clear, readable format.

## Example Usage

After installing `printdirtree`, you can run it to visualize the structure of your project directory. Here's an example command that excludes `.git` files:

```sh
printdirtree --exclude-file ".git"
```

Output for the `PrintDirTree` project might look like this:

```
PrintDirTree
├── MANIFEST.in
├── README.md
├── printdirtree
│   ├── __init__.py
│   └── __main__.py
└── setup.py
```