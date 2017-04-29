#!/bin/sh

cd app
su -m docker-user -c "python app.py"