
from http import HTTPStatus
import http
from app.status_code import MISSING_ARGUMENT
from flask.json import jsonify
from app import db, models
from app.auth.jwt import company_login_required, jwt_auth, require_login
from flask import Blueprint, request

bp = Blueprint('requirement', __name__, url_prefix='/requirement')

@bp.route('/create', methods=['POST'])
@jwt_auth.login_required
@require_login([models.Company])
def create():
    company : models.Company = jwt_auth.current_user()

    data = request.get_json()
    if (data is None):
        return jsonify(message=MISSING_ARGUMENT), HTTPStatus.BAD_REQUEST
        
    template_id = data.get('template_id', None)
    permission = data.get('permission', None)
    optional = data.get('optional', None)

    if (template_id is None or permission is None or optional is None):
        return jsonify(message=MISSING_ARGUMENT), HTTPStatus.BAD_REQUEST

    if (permission not in ['read', 'all']):
        return jsonify(message='请求的权限不合法'), HTTPStatus.BAD_REQUEST

    if (models.Requirement.query.filter_by(company_id = company.id, template_id = template_id).first() != None):
        return jsonify(message='您已提出过该需求'), HTTPStatus.BAD_REQUEST

    requirement = models.Requirement(company.id, template_id, permission, optional)
    db.session.add(requirement)
    db.session.commit()

    if (models.Requirement.query.filter_by(company_id = company.id, template_id = template_id).first() is None):
        return jsonify({'message': '创建失败'}), HTTPStatus.BAD_REQUEST

    return jsonify({'message': '创建成功'}), HTTPStatus.OK


@bp.route('/remove', methods=['POST'])
@jwt_auth.login_required
@require_login([models.Company])
def remove():
    company : models.Company = jwt_auth.current_user()
    
    data = request.get_json()
    if (data is None):
        return jsonify(message=MISSING_ARGUMENT), HTTPStatus.BAD_REQUEST
        
    template_id = data.get('template_id', None)

    if (template_id is None):
        return jsonify(message=MISSING_ARGUMENT), HTTPStatus.BAD_REQUEST

    requirement = models.Requirement.query.filter_by(company_id = company.id, template_id = template_id).first()
    if (requirement is None):
        return jsonify(message='该需求已经不存在'), HTTPStatus.BAD_REQUEST

    db.session.delete(requirement)
    db.session.commit()

    requirement = models.Requirement.query.filter_by(company_id = company.id, template_id = template_id).first()
    if (requirement != None):
        return jsonify(message='删除失败'), HTTPStatus.INTERNAL_SERVER_ERROR

    return jsonify(message='删除成功'), HTTPStatus.OK


@bp.route('/modify', methods=['POST'])
@jwt_auth.login_required
@company_login_required
def modify():
    company : models.Company = jwt_auth.current_user()

    data = request.get_json()
    if (data is None):
        return jsonify(message=MISSING_ARGUMENT), HTTPStatus.BAD_REQUEST
        
    template_id = data.get('template_id', None)
    permission = data.get('permission', None)
    optional = data.get('optional', None)

    if (template_id is None or permission is None or optional is None):
        return jsonify(message=MISSING_ARGUMENT), HTTPStatus.BAD_REQUEST

    if (permission not in ['read', 'all']):
        return jsonify(message='请求的权限不合法'), HTTPStatus.BAD_REQUEST\
    
    requirement = models.Requirement.query.filter_by(company_id = company.id, template_id = template_id).first()
    requirement.permission = permission
    requirement.optional = optional
    db.session.commit()

    return jsonify(message='修改成功'), HTTPStatus.OK
