# PrintDirTree

`printdirtree` is a command-line utility that prints the structure of a directory tree, 
offering the flexibility to specify files and directories to exclude. This tool 
is very useful to aid with prompting ChatGPT. 

## Installation

Install `printdirtree` easily with pip:

```sh
pip install printdirtree
```

## Usage

To use `dirtree`, simply run the command followed by optional arguments to tailor the output to your needs. 
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