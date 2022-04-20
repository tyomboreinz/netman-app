# Netman

IP Address and Portal App Management

## Requirement

Ubuntu / Debian

Package **nmap** already installed

Python 3.9.5

## Installation

Install some requirement for Python using pip

```bash
pip3 install -r requirement.txt
```

Migrate model to database

```bash
python3 manage.py makemigrations
python3 manage.py migrate
```

Then insert default configuration of Portal

```bash
python3 manage.py loaddata data/ConfigPortal.json
```

insert user dan password

```bash
python3 manage.py shell -c "from django.contrib.auth.models import User; User.objects.create_superuser('admin', 'admin@example.com', 'password')"
```

## Run Application

```bash
python3 manage.py runserver 0.0.0.0:8080
```

## Feature

- IP Address Management
- APP Management
- Credential Management
- Group Management
- Portal App
- Ping Scan Ip Address using Nmap