from flask import request, g
from functools import wraps
from werkzeug.exceptions import Forbidden

def validate_schema(schema):
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            request_dict = request.args.copy()
            if request.json:
                request_dict.update(request.json.copy())
            schema_data = schema.load(request_dict)
            return f(schema_data, *args, **kwargs)

        return decorated_function
    return decorator

def auth_token_required(token_header='Authorization', ):
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            validator = g.get('validator', lambda token: False)
            token = request.headers.get(token_header, None)
            playload = validator(token=token)
            if not playload:
                raise Forbidden
        
            kwargs['auth_data'] = playload
            return f(*args, **kwargs)

        return decorated_function
    return decorator