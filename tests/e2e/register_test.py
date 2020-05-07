"""E2E test for Registering"""

import pytest
import requests

from django.contrib.auth import get_user_model
from oauth2_provider.models import Application
from tests.data import populateDB


@pytest.mark.django_db
def test_register_user():
    populateDB()
    User = get_user_model()
    user = User.objects.get(email='test@abc.com')
    assert user.id == 100
    application = Application.objects.get(user_id=user.id)
    assert application.authorization_grant_type == 'password'
    url = "https://localhost:8000/users/register"
    data = {
        "email": "123@123.com",
        "passsword": "password",
        "first_name": "John"}
    response = requests.post(url, data=data, verify=False)
    resp = response.json()
    #activate_link = resp.get("access_token", None)
    assert resp == "foo"

