#!/bin/bash

# Directory to copy repositories to before zipping
backup_dir="all_projects"

# Iterate over all directories in the current directory
for dir in */ ; do
    if [ -d "$dir/.git" ]; then
        echo
        echo "Updating repository in $dir"
        cd "$dir"

        # Get the current branch
        original_branch=$(git rev-parse --abbrev-ref HEAD)

        echo
        echo "Fetching all remotes..."
        git fetch -a

        echo
        echo "Pruning deleted branches..."
        git fetch -p

        echo
        echo "Pulling updates from all remote branches..."
        for branch in $(git branch -r | grep -v '\->'); do
            git checkout "$branch" && git pull
        done

        # Switch back to the original branch
        git checkout "$original_branch"

        # Go back to the parent directory
        cd ..
    else
        echo
        echo "$dir is not a git repository. Skipping..."
    fi
done

echo
echo "All repositories have been updated."

# Create the backup directory if it doesn't exist
if [ -d "$backup_dir" ]; then
    rm -rf "$backup_dir"
fi
mkdir "$backup_dir"

# Ensure all folder permissions are chmod 777
echo
echo "Setting folder permissions to chmod 777..."
for dir in */ ; do
    chmod -R 777 "$dir"
done

# Copy all directories to the backup directory, excluding the backup directory itself
echo
echo "Copying all directories to $backup_dir..."
# rsync -av --exclude=node_modules --exclude=venv --exclude="$backup_dir" */ "$backup_dir"/

# Loop through source folders and copy them to the destination
for dir in */ ; do
    # Copy the folder to the destination
    rsync -aqr --exclude=node_modules --exclude=venv --exclude=runtime --exclude="$backup_dir" --exclude='*.ini' "$dir" "$backup_dir"/"$dir"
    echo "Copied $dir to $backup_dir"
done

# Zip the backup directory
echo
echo "Creating zip file all_projects.zip..."
zip -q -r all_projects.zip "$backup_dir"

# Remove the backup directory after zipping
echo
echo "Removing the backup directory $backup_dir..."
rm -rf "$backup_dir"

echo
echo "All repositories have been backed up and zipped."

echo
echo "Script has completed."