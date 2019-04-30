# Simple python authorization

This module was created to provide a simple authorization method to be used in service to service authorization.

## How to use

**Important note about the credentials backend:** At this moment we do not provide a backend to store credentials. We receive a dict containing all the valid credentials following this format: `{"app_key":["app_name","secret"]}`

Create a middleware in your API that receives the Authorization header and passes it to the package to ensue that the token is valid. In the above example we have a simple endpoint that validates the authentication based on a local dictionary as a credentials backend. Ideally you will implement a credential repository and pass the valid credentials to the module.

```python
from http import HTTPStatus
from flask import request, jsonify, Flask
from python_authorization import Authorization

app = Flask(__name__)

@app.route('/')
def dummy_endpoint():
    authorization_header = request.headers.get('Authorization')

    py_auth = Authorization(authorization_header, valid_credentials_dict={'valid_app_key1': ['valid_app_name', 'valid_secret']})

    # This method will only validate the format of the token
    is_valid = py_auth.validate_token_format()

    if not is_valid:
        return (jsonify({'Message': 'Invalid authorization token format'}), HTTPStatus.UNAUTHORIZED)

    # This method will asume that the token is in a valid format and will try to validate it 
    is_authorized = py_auth.validate_token()

    if not is_authorized:
        return (jsonify({'Message': 'Invalid authorization token'}), HTTPStatus.UNAUTHORIZED)

    return (jsonify({'Message': 'You are in!'}), HTTPStatus.OK)

app.run('0.0.0.0', port=5000)
```

You can also use this module to authenticate at a service using the Credentials class.

```python
from python_authorization import Credentials

credentials_factory = Credentials('valid_app_name', 'valid_app_key1', 'valid_secret')

token = credentials_factory.build_token()

print(f'This is my token: {token}')
```