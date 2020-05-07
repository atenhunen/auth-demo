import pytest
import os
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "auth_demo.settings")
django.setup()

def _mock_config():
    """Mock config."""
    conf = {
    }
    return conf

class ObjectDoesNotExist(Exception):
    pass

class BaseMock(object):
    """BaseMock"""

    def get(self):
        raise ObjectDoesNotExist()



class MockUser(object):
    """Mock user"""

    def __init__(self):
        self.email = '123@123.com'
        self.first_name = None
        self.last_name =  None
        self.password = 'demo123DEMO'
        self.is_active = False

    def save(self):
        """Mock save."""
        pass

class MockAccessToken(object):
    """MockAccessToken"""
    token = 'fPVZG1RaEpcwzJiDkv6ZTZKGHKNrOycccc'

@pytest.fixture()
def mock_user_registered():
    """Mock configs for unit testing."""
    user = MockUser()
    return user

@pytest.fixture()
def mock_user_active():
    """Mock configs for unit testing."""
    user = MockUser()
    user.is_active = True
    return user

@pytest.fixture()
def mock_access_token():
    """Mock configs for unit testing."""
    token = MockAccessToken()
    return token