#!/bin/bash

# Ask for a commit message
echo "Enter commit message:"
read msg

# Run git commands
git add .
git commit -m "$msg"
git push origin main