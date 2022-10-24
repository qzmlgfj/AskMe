from functools import wraps
from flask import jsonify, current_app, request
import jwt

from .orm.admin import Admin

def token_required(f):
    @wraps(f)
    def _verify(*args, **kwargs):
        auth_headers = request.headers.get('token', '').split()

        invalid_msg = {
            'message': 'Invalid token. Registeration and / or authentication required',
            'authenticated': False
        }
        expired_msg = {
            'message': 'Expired token. Reauthentication required.',
            'authenticated': False
        }

        if len(auth_headers) != 1:
            return jsonify(invalid_msg), 401

        try:
            token = auth_headers[0]
            data = jwt.decode(token, current_app.config['SECRET_KEY'], algorithms=['HS256'])
            user = Admin.query.filter_by(username=data['username']).first()
            if not user:
                raise RuntimeError('User not found')
            return f(*args, **kwargs)
        except jwt.ExpiredSignatureError:
            return jsonify(expired_msg), 401 # 401 is Unauthorized HTTP status code
        except (jwt.InvalidTokenError, Exception) as e:
            print(e)
            return jsonify(invalid_msg), 401

    return _verify