#!/bin/sh

su -m docker-user -c "celery worker -A runcelery.celery"