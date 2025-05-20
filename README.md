# Gimnasio Backend - API REST (Django + MariaDB)

Este proyecto es la API REST del sistema de gestión de un gimnasio. Gestiona usuarios, clases, horarios, publicaciones, comentarios, suscripciones y pagos mediante PayPal.

## ¿Por qué es útil?

- Permite a los monitores crear y gestionar clases y horarios.
- Los clientes pueden inscribirse, comentar y suscribirse mediante pagos.
- Incluye control de acceso según roles (cliente y monitor).
- Totalmente dockerizado y desplegado en AWS EC2 con MariaDB.

---

## Enlace de acceso a la API (producción), (solo funciona cuando el laboratorio de aws está arrancado)

> [http://54.86.178.93:8000](http://54.86.178.93:8000)

---

## Tecnologías utilizadas

- Python 3.12
- Django 5
- Django REST Framework + Simple JWT
- MariaDB 10.7
- Docker & Docker Compose
- AWS EC2

---

## Instalación local (desarrollo)

### 1. Clona el repositorio:

git clone https://github.com/fraangorrionn/GimnasioDjango.git
cd gimnasio

### 2. Crea un entorno virtual y actívalo:

python -m venv myvenv
source myvenv/bin/activate

### 3. Instala dependencias:

pip install -r requirements.txt

### 4. Configura tu base de datos (MariaDB) y actualiza settings.py:

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'gimnasio',
        'USER': 'usuario',
        'PASSWORD': '2004',
        'HOST': 'localhost',
        'PORT': '3306',
    }
}

### 5. Ejecuta migraciones y servidor:

python manage.py migrate
python manage.py runserver


## Despliegue en producción (Docker + AWS)

### 1. Crea y sube tu imagen a Docker Hub:
docker build -t fraangorrionn/gimnasiobackend:v5 .
docker push fraangorrionn/gimnasiobackend:v5

### 2. En tu instancia EC2 (54.86.178.93), crea este docker-compose.yml:
version: '3'
services:
  mariadb:
    image: mariadb:10.7
    environment:
      MYSQL_DATABASE: gimnasio
      MYSQL_USER: usuario
      MYSQL_PASSWORD: 2004
      MYSQL_ROOT_PASSWORD: rootpass
    volumes:
      - db_data:/var/lib/mysql
    ports:
      - "3306:3306"

  backend:
    image: fraangorrionn/gimnasiobackend:v
    depends_on:
      - mariadb
    environment:
      - DEBUG=True
      - DB_NAME=gimnasio
      - DB_USER=usuario
      - DB_PASSWORD=2004
      - DB_HOST=mariadb
      - DB_PORT=3306
    ports:
      - "8000:8000"

volumes:
  db_data:


### 3. Levanta los servicios:

sudo docker compose up -d

## Soporte

Si tienes dudas o encuentras errores, puedes contactarme a través de GitHub:
[fraangorrionn](https://github.com/fraangorrionn)

## Documentación adicional

Puedes consultar el documento detallado del proyecto aquí:  
[Documento del Proyecto (Google Docs)](https://docs.google.com/document/d/1XSjxUyFBwzG6Lz1Mr-ADLLDHurLNNChOs62Wp-NC-KQ/edit?usp=sharing)

## Autor
Nombre: Francisco

GitHub: fraangorrionn

