#!/bin/bash
set -ex
#init git while new created
if [! -d "/app/.git"]
then
    echo "Directory .git DOES NOT exists."
    git int
fi
sudo chown user:user /app -R