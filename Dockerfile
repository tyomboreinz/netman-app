FROM python:alpine

COPY . /app

WORKDIR /app

RUN mkdir /app/static/images/app && \
    chmod +x entrypoint.sh &&\
    apk update && \
    apk add nmap tk && \
    pip install --upgrade pip && \
    pip3 install -r requirement.txt

RUN python3 manage.py makemigrations && \
    python3 manage.py migrate && \
    python3 manage.py loaddata data/data.json && \
    python3 manage.py shell -c "from django.contrib.auth.models import User; User.objects.create_superuser('admin', 'admin@example.com', 'password')"

EXPOSE 8080

ENTRYPOINT [ "sh", "/app/entrypoint.sh" ]