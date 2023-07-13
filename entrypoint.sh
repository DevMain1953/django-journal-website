#!/bin/bash

# Start Celery
celery -A website worker -l info

# Run Django server
python3.11 manage.py runserver 127.0.0.1:8000