# Quick Git Repo Backup

A bash script that automates the process of updating and backing up multiple Git repositories in a directory.

## Features

- Updates all Git repositories in the current directory
- Tracks and updates all remote branches
- Disables file permission tracking for each repository
- Creates a backup zip file of all repositories
- Excludes unnecessary files and directories (node_modules, venv, runtime, .ini files)
- Sets appropriate permissions (777) for all directories

## Usage

1. Place the script in the parent directory containing your Git repositories
2. Make the script executable:
   ```bash
   chmod +x quick_git_repo_backup.sh
   ```
3. Run the script:
   ```bash
   ./quick_git_repo_backup.sh
   ```

## What it does

1. For each Git repository in the current directory:

   - Disables file permission tracking
   - Tracks all remote branches
   - Fetches updates from all remotes
   - Prunes deleted branches
   - Pulls updates from all remote branches
   - Returns to the original branch

2. Creates a backup:
   - Creates a temporary directory called "all_projects"
   - Sets directory permissions to 777
   - Copies all repositories to the backup directory
   - Creates a zip file (all_projects.zip)
   - Removes the temporary backup directory

## Excluded Files/Directories

The script automatically excludes the following:

- node_modules/
- venv/
- runtime/
- \*.ini files
- The backup directory itself

## Output

The script creates a file called `all_projects.zip` containing all your repositories with their latest updates.

## Requirements

- Bash shell
- Git
- rsync
- zip utility
