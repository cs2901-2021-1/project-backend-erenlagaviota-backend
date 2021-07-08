from functools import wraps

import json
from flask import request
from flask import Response


def auth_required(function):
    """
    Verify authentication header in every request
    """
    @wraps(function)
    def authenticated(*args, **kwargs):
        auth = request.authorization
        # TODO:  <08-07-21, Mario> Get the username and password from database (ours)
        if auth and auth.username == 'prueba' and auth.password == 'prueba':
            return function(*args, **kwargs)
        return Response(json.dumps({'message': 'Not authorized'}), status=401, content_type='application/json')

    return authenticated
