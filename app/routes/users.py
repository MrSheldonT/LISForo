from flask import Blueprint, request, jsonify
from app.services.user_service import create_user, login_user, update_user, show_user
from app.utils.token_management import token_required

user_bp = Blueprint("users", __name__)

@user_bp.route("/register", methods=['POST'])
def register():
    data = request.json
    status_new_user = create_user(data)
    if status_new_user['success'] == True:
        return jsonify(status_new_user), 200
    
    return jsonify(status_new_user), 401

@user_bp.route('/login', methods=['POST'] )
def login():
    data = request.json
    status_login = login_user(data)

    if status_login['success'] == True:
        return status_login, 201
    else:
        return status_login, 400

@user_bp.route('/update_password', methods=['PATCH'])
@token_required
def update_password():
    data = request.json

    if not data or 'password' not in data or len(data) != 1:
        return jsonify({'success': False,'message': "Only password field is allowed and required"}), 400

    new_password = data['password']
    status_update_password = update_user({'id_user': request.id_user, 'password': new_password})
    
    return jsonify(status_update_password)

@user_bp.route('/show_user', methods=['GET'])
@token_required
def show_user_info():
    status_user = show_user({'id_user': request.id_user, 'id_role': request.id_role})

    return jsonify(status_user)
