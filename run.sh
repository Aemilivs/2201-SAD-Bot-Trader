#!/bin/sh

sh API/run.sh &
python3.10 Flask-UI/run.py &