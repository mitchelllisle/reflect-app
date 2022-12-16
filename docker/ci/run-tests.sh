#!/usr/bin/env sh
set -e

sudo python -m pip install --upgrade pip
sudo python -m pip install -U pip setuptools

sudo pip install --user -r requirements/tests.txt
sudo pip install --user .

sudo python -m pytest --headless --cov=reflect
