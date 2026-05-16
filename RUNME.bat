@echo off

::start .\side.bat
%python312% runbrowser.py global
%python312% manage.py runserver 0.0.0.0:8000
