"""Views.py test"""
import auth_demo.models.utils

from auth_demo.api.views import generate_activation_link

def test_activation_link(mock_user_registered):
    """Test activation link generation."""

    setattr(
        auth_demo.models.utils,
        'get_if_exists',
        lambda x, email=None: mock_user_registered)
    result, token = generate_activation_link('123@123.com', 'https://localhost')
    assert token not in ["", None, []]
    assert result == f'https://localhost/activate/{token}'

