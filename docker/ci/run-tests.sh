#!/usr/bin/env sh
set -e

cd source
sudo pip install --user -r requirements/test.txt
sudo pip install --user .

sudo python -m pytest --headless --cov=reflect
