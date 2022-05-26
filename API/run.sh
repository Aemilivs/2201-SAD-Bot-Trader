#!/bin/sh
# A script to launch the flask application.
#running on Mac might be problematic, ensure greadlink is installed on MAC
FLASK_APP="$(readlink -f API/__main__.py || greadlink -f API/__main__.py)"
FLASK_ENV=development
export FLASK_APP
export FLASK_ENV
flask run