#!/bin/sh
# A script to launch the flask application.
FLASK_APP=$(readlink -f main.py)
FLASK_ENV=development
export FLASK_APP
export FLASK_ENV
flask run