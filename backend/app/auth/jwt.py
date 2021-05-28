from functools import wraps
from itsdangerous import BadSignature, SignatureExpired, TimedJSONWebSignatureSerializer as Serializer
from app.models import Company, User, Admin
from app.status_code import FORBIDDEN, UNAUTHORIZED
from flask import current_app
from flask.json import jsonify
from flask_httpauth import HTTPTokenAuth
from http import HTTPStatus

jwt_auth = HTTPTokenAuth()

def generate_jwt_token_for_user(user : User):
    return generate_jwt_token({'user_id': user.id})


def generate_jwt_token_for_company(company : Company):
    return generate_jwt_token({'company_id': company.id})


def generate_jwt_token_for_admin(admin : Admin):
    return generate_jwt_token({'admin_id': admin.id})


def generate_jwt_token(dic : dict, expires_in=current_app.config['JWT_EXPIRES_SECOND']):
    s = Serializer(current_app.config['JWT_SECRET_KEY'], expires_in=expires_in)
    token = s.dumps(dic).decode('utf-8')

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

        if user is not None:
            return user
    if 'company_id' in data:
        company_id = data['company_id']
        company = Company.query.get(company_id)

        if company is not None:
            return company
    if 'admin_id' in data:
        admin_id = data['admin_id']
        admin = Admin.query.get(admin_id)

        if admin is not None:
            return admin
    if 'oauth_access_token' in data:
        content = data

        return content
    if 'refresh_token' in data:
        content = data

        return content

    return False


@jwt_auth.error_handler
def error_handler():
    return jsonify(message = UNAUTHORIZED), HTTPStatus.UNAUTHORIZED

def require_login(typings):
    def decorator(f):
        @wraps
        def wrapper():
            user = jwt_auth.current_user()

            if (type(user) in typings):
                return f()
            
            return jsonify(message = FORBIDDEN), HTTPStatus.FORBIDDEN
    
        return wrapper
    return decorator

def user_login_required(f):
    @wraps(f)
    def wrapper():
        user = jwt_auth.current_user()

        if (isinstance(user, User)):
            return f()

        return jsonify(message = FORBIDDEN), HTTPStatus.FORBIDDEN
    
    return wrapper


def company_login_required(f):
    @wraps(f)
    def wrapper():
        user = jwt_auth.current_user()

        if (isinstance(user, Company)):
            return f()

        return jsonify(message = FORBIDDEN), HTTPStatus.FORBIDDEN
    
    return wrapper

def admin_login_required(f):
    @wraps(f)
    def wrapper():
        user = jwt_auth.current_user()

        if (isinstance(user, Admin)):
            return f()

        return jsonify(message = FORBIDDEN), HTTPStatus.FORBIDDEN
    
    return wrapper

def refresh_token_required(f):
    @wraps(f)
    def wrapper():
        data = jwt_auth.current_user()

        if 'refresh_token' in data:
            return f()

        return jsonify(message = FORBIDDEN), HTTPStatus.FORBIDDEN
    
    return wrapper

def auth_access_token_required(f):
    @wraps(f)
    def wrapper():
        data = jwt_auth.current_user()

        if 'oauth_access_token' in data:
            return f()

        return jsonify(message = FORBIDDEN), HTTPStatus.FORBIDDEN
    
    return wrapper
