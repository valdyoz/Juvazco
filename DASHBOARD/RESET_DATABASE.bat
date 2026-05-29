@echo off
title RESET DATABASE
del db.sqlite3 2>nul
del shop\migrations\0001_initial.py 2>nul
del shop\migrations\0002*.py 2>nul
del shop\migrations\0003*.py 2>nul
python manage.py makemigrations
python manage.py migrate
pause
