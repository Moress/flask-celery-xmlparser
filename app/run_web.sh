#!/bin/sh

if [ ! -d "$UPLOAD_FOLDER" ]; then
  su -m docker-user -c "mkdir $UPLOAD_FOLDER"
fi

if [ ! -d "migrations" ]; then
    su -m docker-user -c "python app.py db init"
fi

if [ -f "app.db" ]; then
    su -m docker-user -c "python app.py db migrate"
fi

su -m docker-user -c "python app.py db upgrade"
su -m docker-user -c "python app.py runserver -h 0.0.0.0"