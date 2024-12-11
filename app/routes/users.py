from flask import Blueprint, request, jsonify
from app.services.user_service import create_user, login_user, update_user, show_user
from app.utils.token_management import token_required

user_bp = Blueprint("users", __name__)

@user_bp.route("/register", methods=['POST'])
def register():

    data = request.json
    if not data or 'username' not in data or 'password' not in data or 'email' not in data:
        return jsonify({'success': False, 'message': "Parameters not provided (username, password, email)"}), 400
    
    status_new_user = create_user(data)
    if status_new_user['success'] == True:
        return status_new_user, 200
    
    return status_new_user, 400

@user_bp.route('/login', methods=['POST'] )
def login():
    data = request.json
    print(data)
    if not data or 'username' not in data or 'password' not in data:
        print(not data)
        print('username' not in data)
        return jsonify({'success': False, 'message': "Parameters not provided (username, password)"}), 400
    
    status_login = login_user(data)

    if status_login['success'] == True:
        return status_login, 200
    
    return status_login, 400

@user_bp.route('/update_password', methods=['PATCH'])
@token_required
def update_password():
    data = request.json
    data['id_user_request'] = request.id_user
    if not data or 'password' not in data or not 'id_user_account' in data or not 'id_user_request' in data: #no enviar algo como id_role o password
        return jsonify({'success': False, 'message': "Parameters not provided (id_user_request, password, id_user)"}), 400

    status_update_password = update_user(data)
    if status_update_password['success'] == True:
        return status_update_password, 200
    
    return status_update_password, 400

@user_bp.route('/show_user', methods=['GET'])
@token_required
def show_user_info():
    id_user = request.args.get('id_user', default=request.id_user, type=int)
    status_user = show_user({'id_user': id_user})
    if status_user['success'] == True:
        return status_user, 200
    
    return status_user, 400

@user_bp.route('/change_role', methods=['PATCH'])
@token_required
def change_role():
    data = request.json
    data['id_user_request'] = request.id_user
    if not data or 'id_role' not in data or not 'id_user_account' in data or not 'id_user_request' in data:
        return jsonify({'success': False, 'message': "Parameters not provided (id_user_request, id_role)"}), 400

    if data['id_user_account'] == data['id_user_request']:
        return jsonify({'success': False, 'message': "You can only change the role of users other than yourself"}), 400
    status_update_role = update_user(data)
    if status_update_role['success'] == True:
        return status_update_role, 200
    
    return status_update_role, 400