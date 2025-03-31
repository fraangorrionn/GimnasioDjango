# GimnasioDjango
sudo apt-get install python3-venv  -> Sino está instalado ya
Creamos el archivo .gitignore correspondiente a proyectos Django
Creamos el archivo requirements.txt con la versión de Django
python3 -m venv myvenv -> Creamos el entorno
source myvenv/bin/activate
python -m pip install --upgrade pip
pip install -r requirements.txt
Creamos la configuración de Django: django-admin startproject mysite .
Realizamos los cambios correspondientes en settings.py
python manage.py migrate -> Hacemos la migración
python manage.py startapp <nombre_app>
Y probamos que funciona: python manage.py runserver 127.0.0.1:8080
