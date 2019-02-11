#!/bin/bash

# Exit with fail if any command in this script fails
set -e

cd /elpis
apt-get install python3-venv
python3 -m venv venv_test
source venv_test/bin/activate
pip install pytest
pip install -r requirements.txt
alias pytest=venv_test/bin/pytest
pytest

# Test React and Javascript code

echo 'Testing done.'