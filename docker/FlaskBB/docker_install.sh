#!/usr/bin/env bash

docker rm -f install_flaskbb

docker run \
    -h install_flaskbb \
    --name install_flaskbb \
    -d \
    python:2.7 sh -c "while true
do
date +'%Y-%m-%d %H:%M:%S'
sleep 1
done"


git clone https://github.com/sh4nks/flaskbb.git
cd flaskbb
git checkout 2.0.0
virtualenv .venv -p python3
source .venv/bin/activate
pip install -U pip setuptools==45.2.0       # Fix Feature Install
pip install -r requirements.txt
