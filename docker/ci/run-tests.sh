#!/usr/bin/env sh
set -e

sudo pip install --user -r requirements/tests.txt
sudo pip install --user .

sudo python -m pytest --headless --cov=reflect
