#!/bin/bash

# default configs
PORT=5000
HOST=127.0.0.1
SOCK=/tmp/app.sock
WORKERS=4

# activate the virtualenv file
source env/bin/activate

#check for the type of the application we want to run
if [[ $1 ==  "develop" ]]; then
    export FLASK_ENV=development
    export FLASK_APP=app
    flask run --host $HOST --port $PORT
else
    export FLASK_ENV=production
    gunicorn app:app --bind unix:$SOCK -w $WORKERS
fi

