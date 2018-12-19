#!/bin/bash

# Exit with fail if any command in this script fails
set -e

# Test python project
source venv/bin/activate
export PYTHONPATH=`pwd`/..
pytest

# Test React and Javascript code

echo 'Testing done.'