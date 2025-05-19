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
pip install mysqlclient
sudo apt install libmariadb-dev pkg-config
sudo apt install mariadb-client
sudo systemctl start mariadb


sudo mariadb -u usuario -p
USE gimnasio;
SELECT id, username, email, rol FROM gimnasio_usuario;
SELECT * FROM gimnasio_clase;
