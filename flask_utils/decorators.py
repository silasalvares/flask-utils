from flask import request
from functools import wraps

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

def auth_token_required(roles=[]):
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            auth_token = request.headers.get('Authentication-Token', None)
            
            if auth_token is not None:
                decoded_token = jwt_handler.decode_token(auth_token)
                user_roles = decoded_token.get('roles', [])
                matched_roles = [r for r in roles if r in user_roles]
                if len(roles) == 0 or len(matched_roles) > 0:
                    return f(decoded_token, *args, **kwargs)
                else:
                    raise Forbidden
            else:
                raise InvalidToken

        return decorated_function
    return decorator