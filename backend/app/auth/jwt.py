from flask.json import jsonify
from itsdangerous import BadSignature, SignatureExpired, TimedJSONWebSignatureSerializer as Serializer
from app.models import User
from flask import current_app
from flask_httpauth import HTTPTokenAuth

jwt_auth = HTTPTokenAuth()

def generate_jwt_token(user : User):
    s = Serializer(current_app.config['JWT_SECRET_KEY'], expires_in=current_app.config['JWT_EXPIRES_SECOND'])
    token = s.dumps({'user_id': user.id}).decode('utf-8')

    return token


@jwt_auth.verify_token
def verify_token(token):
    s = Serializer(current_app.config['JWT_SECRET_KEY'])

    try:
        data = s.loads(token)
    except SignatureExpired:
        return False
    except BadSignature:
        return False
    
    if 'user_id' in data:
        user_id = data['user_id']
        user = User.query.get(user_id)
        # user = User.query.filter_by(id=user_id)
        print("dic", user.to_dict())

        if user is not None:
            return user

    return False


@jwt_auth.error_handler
def error_handler():
    return jsonify({'code':401, 'message':'401 Unauthorized Access'})
