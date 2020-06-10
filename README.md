# OAuth2 API with Django and Django REST Framework

This repo demonstrates an OAuth2 based authorization for accessing a user information. Core stack consists of Python 3.7, Django 3, Django REST Framework and Django Oauth2 Provider.

# Installation

## Create virtualenv

First install virtualenv
```bash
$ cd auth-demo
$ sudo python3 -m pip install virtualenv
```

then, create virtualenv
```bash
$ python3 -m venv venv
```

then, install test dependencies to virtual env
```bash
$ venv/bin/pip3 install -r requirements.txt
$ venv/bin/pip3 install -r testing_requirements.txt
```

migrate database
```bash
sudo venv/bin/python3 manage.py migrate
```
Run test server
```bash
$ sudo venv/bin/python3 manage.py runsslserver
```

## Create superuser
```bash
$ sudo PYTHONPATH=. venv/bin/python3 manage.py createsuperuser
```

## Register client

In order to get a valid access_token we must register an OAuth application first. Go to Django admin
http://localhost:8000/o/applications/

Login with superuser credentials you just created.

Create new application and fill the form

    Name: Some name

    Client Type: confidential

    Authorization Grant Type: Resource owner password-based

We are ready now, OAuth can be tested.

Note! This application will be used across this demo.
Note! Ensure this application has id=1, this is a quick test fix.

## Test manually the APIs

### Register new user
```bash
$ curl -k -X POST -d '{"email": "abc123@abc.com", "first_name": "John", "password": "Demo1234"}' -H "Content-Type: application/json" https://localhost:8000/users/register

    {"email":"abc123@abc.com","first_name":"John","last_name":null}
```
You should receive now the activation link in email and also in django server stdout for debug purposes.

### Activate user
Click the link received in email and open it in browser, see example below.

https://localhost/activate/je1zpxjEn9Il

Next we can login user and receive OAuth Bearer token in exchange.
```bash
$ curl -k -X POST -d '{"password": "Demo1234", "email": "abc123@abc.com"}' -H "Content-Type: application/json" https://localhost:8000/login/

    {"message":"Access granted","access_token":"uyVHBU2JykOkAY03hVADt9kZ4sbrhy"}
```

User is now ready to user OAuth2 services. First, lets try to change password:
```bash
$ curl -k -X PUT -d '{"new_password": "Demo9000"}' -H "Authorization: Bearer uyVHBU2JykOkAY03hVADt9kZ4sbrhy" -H "Content-Type: application/json" https://localhost:8000/update-password/
```
Password is now changed, let's test it, following should fail:
```bash
$ curl -k -X POST -d '{"password": "Demo1234", "email": "abc123@abc.com"}' -H "Content-Type: application/json" https://localhost:8000/login/

    {"message":"Authentication failed"}

```
New password should work instead, lets try:
```bash
$ curl -k -X POST -d '{"password": "Demo9000", "email": "abc123@abc.com"}' -H "Content-Type: application/json" https://localhost:8000/login/

    {"message":"Access granted","access_token":"TcYMI3yUXSqBql4P8nOLOD3yFCklEX"}
```

Let's see if we can access the users API:
```bash
$ curl -k -X GET -H "Authorization: Bearer uyVHBU2JykOkAY03hVADt9kZ4sbrhy" -H "Content-Type: application/json" https://localhost:8000/users/1/

    {"username":"","email":"abc123@abc.com","first_name":"","last_name":""}

$ curl -k -X GET -H "Authorization: Bearer uyVHBU2JykOkAY03hVADt9kZ4sbrhy" -H "Content-Type: application/json" https://localhost/8000/users/
[
   {
      "username":"",
      "email":"my.mail@gmail.com",
      "first_name":"",
      "last_name":""
   },
   {
      "username":"",
      "email":"abc123@abc.com",
      "first_name":"",
      "last_name":""
   }
]
```
Without bearer token we wont see email, just first name.
```bash
$ curl -k -X GET -H "Content-Type: application/json" https://localhost:8000/users/1/

    {"first_name":"John"}
```

## Run tests

then, install test dependencies to virtual env
```bash
$ venv/bin/pip3 install -r testing_requirements.txt
```

in order to run unit tests with integration tests, add write permissions to DB
```bash
$ sudo chmod 664 db.sqlite3
```

Then run the tests
```bash
$ PYTHONPATH=. venv/bin/py.test -vv
```

NOTE! integraion tests with DB are still in the works.

## Oauth2 API
localhost:8000/o/ has OAuth API for for creating bearer token. This is used under
the actual solution API and can be tested separately.

### Get token
We can try with curl to grant access and get token.
```bash
$ curl -k -X POST -d "grant_type=password&username=<username>&password=<password>" -u"clientID:<clientSecret>" https://localhost:8000/o/token/
```
response:
```bash
{"access_token": "36NaxnPRvd8kH5WfBACZP3NV8lH4PH", "expires_in": 36000, "token_type": "Bearer", "scope": "read write groups", "refresh_token": "BBnta0A1zHdgC1Y8mApg7OXy9yCQA2"}
```

access_token field now reveals the OAuth token. This can be used to access data.

### Access API with token
```bash
$ curl -H "Authorization: Bearer <your_access_token>" https://localhost:8000/users/
```

### Refresh token
```bash
$ curl -k -X POST -d "grant_type=refresh_token&refresh_token=<refresh-token>&client_id=<client-id>&client_secret=<client-secret>" https://localhost:8000/o/token/
```

response:
```bash
{"access_token": "K0GltFYwwXBZJPd2Yw4wiF919Q0sBZ", "expires_in": 36000, "token_type": "Bearer", "scope": "read write groups", "refresh_token": "CPQ7GPXmIyun0uXVQ4P2CdDN0PkPDI"}
```

## Running with production settings

### Gunicorn
cd auth-demo
source venv/bin/activate
gunicorn auth_demo.wsgi –workers=4 --bind 0.0.0.0:443 --certfile=<path-to-my-cert> --keyfile=<path-to-my-key>

### Docker and Gunicorn
sudo docker build -t auth-demo --tag flask_gunicorn_app .
sudo docker run --privileged --expose 8000 443 auth-demo