Под Windows

python -m venv .venv
cmd
.venv\scripts\activate.bat
pip install django==5.2.18

django-admin startproject threads_sorting
cd threads_sorting
python manage.py startapp sorter

Запуск:
python manage.py migrate
python manage.py runserver

http://127.0.0.1:8000/
