#!/bin/bash
cd ~/Desktop/pisecuritysystem
git pull origin master
workon cv
python livestream.py &
python app.py &
