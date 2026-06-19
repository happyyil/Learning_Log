@echo off
set DEBUG=True

conda activate ll
python manage.py runserver
python runbrowser.py
