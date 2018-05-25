#!/bin/bash
cd ~/Desktop/pisecuritysystem
git pull origin master
source ~/.profile
workon cv
python app.py
