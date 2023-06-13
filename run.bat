@echo off

call venv\Scripts\activate
cd .\Note\
python manage.py runserver

pause