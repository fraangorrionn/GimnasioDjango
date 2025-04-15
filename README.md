# GimnasioDjango
sudo apt-get install python3-venv
python3 -m venv myvenv
source myvenv/bin/activate
python -m pip install --upgrade pip
pip install -r requirements.txt
django-admin startproject mysite .
python manage.py migrate
python manage.py startapp <nombre_app>
python manage.py runserver 127.0.0.1:8080
python manage.py runserver
