#Register client

In order to get a valid access_token we must register an application first. Go to Django admin
http://localhost:8000/o/applications/

Create new application and fill the form

    Name: Some name

    Client Type: confidential

    Authorization Grant Type: Resource owner password-based

We are ready now, OAuth can be tested.

Note! this application will be used accross this demo.
Note! Ensure this application has id=1

#Get token
We can try with curl to grant access and get token.
```bash
curl -k -X POST -d "grant_type=password&username=<username>&password=<password>" -u"clientID:<clientSecret>" https://localhost:8000/o/token/
```
response:
```bash
{"access_token": "36NaxnPRvd8kH5WfBACZP3NV8lH4PH", "expires_in": 36000, "token_type": "Bearer", "scope": "read write groups", "refresh_token": "BBnta0A1zHdgC1Y8mApg7OXy9yCQA2"}
```

access_token field now reveals the OAuth token. This can be used to access data.

Access API with token
```bash
curl -H "Authorization: Bearer <your_access_token>" https://localhost:8000/users/
```

#Refresh token
```bash
curl -k -X POST -d "grant_type=refresh_token&refresh_token=<refresh-token>&client_id=<client-id>&client_secret=<client-secret>" https://localhost:8000/o/token/
```

response:
```bash
{"access_token": "K0GltFYwwXBZJPd2Yw4wiF919Q0sBZ", "expires_in": 36000, "token_type": "Bearer", "scope": "read write groups", "refresh_token": "CPQ7GPXmIyun0uXVQ4P2CdDN0PkPDI"}
```

# Run tests
First install virtualenv
```bash
cd auth-demo
sudo python3 -m pip install virtualenv
```

then, create virtualenv
```bash
python3 -m venv venv
```

then, install test dependencies to virtual env
```bash
venv/bin/pip3 install -r test_requirements.txt
```

in order to run unit tests with integration tests, add write permissions to DB
```bash
sudo chmod 664 db.sqlite3
```

Then run the tests
```bash
PYTHONPATH=. venv/bin/py.test -vv
```