"""Test for users API."""
import pytest
import auth_demo.api.users

from auth_demo.api.users import authenticate_bearer_token


def test_ok_authenticate_bearer_token(mock_user_active, mock_access_token):

    request = {
        '_request': {
            'HTTP_AUTHORIZATION': f'Bearer fPVZG1RaEpcwzJiDkv6ZTZKGHKNrOycccc'}
    }
    setattr(auth_demo.api.users, 'get_token_or_none', lambda **x: mock_access_token)
    setattr(auth_demo.api.users, 'get_user_or_none', lambda **x: mock_user_active)
    assert authenticate_bearer_token(request) == True

def test_failed_authenticate_bearer_token(mock_user_active, mock_access_token):
    request = {
        '_request': {
            'HTTP_AUTHORIZATION': f'Bearer foo'}
    }
    setattr(auth_demo.api.users, 'get_token_or_none', lambda **x: None)
    setattr(auth_demo.api.users, 'get_user_or_none', lambda **x: mock_user_active)
    assert authenticate_bearer_token(request) == False
