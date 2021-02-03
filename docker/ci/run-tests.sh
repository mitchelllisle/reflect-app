#!/usr/bin/env sh
set -e

sudo python3 -m pip install --upgrade pip
sudo python3 -m pip install -U pip setuptools

sudo pip3 install --user -r requirements/tests.txt
sudo pip3 install --user .

sudo python3 -m pytest --headless --cov=reflect
