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

class MockUser(object):
    """Mock user"""

    def __init__(self):
        self.email = '123@123.com'
        self.first_name = None
        self.last_name =  None
        self. password = 'demo123DEMO'

    def save(self):
        """Mock save."""
        pass

@pytest.fixture()
def mock_user_registered():
    """Mock configs for unit testing."""
    user = MockUser()
    return user