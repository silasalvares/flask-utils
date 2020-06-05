from flask import Flask, jsonify
from werkzeug.exceptions import default_exceptions

def make_json_webapi(app_name, **kwargs):
    
    def make_json_error(ex):
        error = str(ex)
        if not str(error):
            error = 'Internal Server Error' 
        error += ' ' + str(type(ex))
        return make_default_response(success=False, errors=[error])

    flask_app = Flask(app_name)
    for exception in default_exceptions.items():
        flask_app.register_error_handler(exception[0], make_json_error)
    
    flask_app.register_error_handler(Exception, make_json_error)

    @flask_app.after_request
    def set_content_type(response):
        if not response.mimetype == 'image/png':
            response.headers["Content-Type"] = "application/json"
        return response

    return flask_app

def make_default_response(success=True, data={}, messages=[], errors=[]):
    return {
        'success': success,
        'data': data,
        'messages': messages,
        'errors': errors
    }