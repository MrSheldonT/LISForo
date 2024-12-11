from flask import Blueprint, jsonify, request
from app.services.role_service import get_users_by_rol
from app.utils.token_management import token_required
roles_bp = Blueprint('roles', __name__)

@roles_bp.route("/", methods=['GET'])
def setRoles():
    return jsonify({'success': True, 'message': "The roles is uploaded"}), 200

@roles_bp.route("/show_roles", methods=['GET'])
@token_required
def show_roles():

    id_role = request.args.get('id_rol', type=int)
    if not id_role:
        return jsonify({'success': False, 'message': "The id_rol is not provided"}), 400

    status_show_roles = get_users_by_rol(id_role)
    if status_show_roles['success'] == True:
        return status_show_roles, 200
    
    return status_show_roles, 500