#!/bin/bash

# Ask for a commit message
echo "enter  the files need to add"
read file
echo "Enter commit message:"
read msg


# Run git commands
git add $file
git commit -m "$msg"
git push origin main