#!/bin/bash

source /home/dev/venv/bin/activate
cd /home/dev/esialogin/
uwsgi --ini /home/dev/esialogin/system/uwsgi.ini
