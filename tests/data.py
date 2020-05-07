"""Test data."""


DATA = {
    'User': {
        "_path": "auth_demo.models.user",
        "data": [{"id": 100, "email": "test@abc.com"}]},
    'Application': {
        "_path": "oauth2_provider.models",
        "data": [
            {"client_type": "confidential",
             "authorization_grant_type": "password",
             "user_id": 100}]
        }
    }


def populateDB():
    for model_name in DATA:
        print(f'importing {model_name}')
        mod = __import__(DATA[model_name]["_path"], fromlist=[model_name])
        model = getattr(mod, model_name)
        for item in DATA[model_name]["data"]:
            print(f'creating {item}')
            model.objects.get_or_create(**item)