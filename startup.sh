#!/bin/bash

gunicorn --bind=0.0.0.0 --timeout 600 --worker-class uvicorn.workers.UvicornWorker backend.main:app