FROM python:3.7
ADD . /auth-demo
WORKDIR /auth-demo
RUN venv/bin/activate
RUN pip3 install -r requirements.txt
EXPOSE 443 8000
CMD ["gunicorn", "auth_demo.wsgi", "–workers=4", "--bind 0.0.0.0:443", "--certfile=/Users/aarnotenhunen/scratch/auth-demo/venv/lib/python3.7/site-packages/sslserver/certs/development.crt", "--keyfile=/Users/aarnotenhunen/scratch/auth-demo/venv/lib/python3.7/site-packages/sslserver/certs/development.key"]
