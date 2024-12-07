from flask import Blueprint, request, jsonify
from app.services.post_service import create_post, show_post, update_post, delete_post
from app.utils.token_management import token_required

post_bp = Blueprint('posts', __name__)

@post_bp.route("/publish_post", methods=['POST'])
@token_required
def publish_post():
    data = request.json
    data['id_user'] = request.id_user            
    status_new_post = create_post(data)
    if status_new_post['success'] == True:
        return status_new_post, 200
    
    return status_new_post, 401

@post_bp.route("/show_post/<int:id_post>", methods=['GET'])
@token_required
def show_post_data(id_post):
    status_post = show_post({'id_post': id_post})
    if status_post['success'] == True:
        #return status_post['post']['content']
        return status_post, 200
    
    return status_post, 401

@post_bp.route("/update_post", methods=['PATCH'])
@token_required
def update_post_data():
    data = request.json
    data['id_user'] = request.id_user
    data['id_role'] = request.id_role
    
    status_post = update_post(data)

    if status_post['success'] == True:
        return status_post, 200
    
    return status_post, 401

@post_bp.route("/delete_post", methods=['DELETE'])
@token_required
def delete_post_data():
    data = request.json
    data['id_user'] = request.id_user
    data['id_role'] = request.id_role

    status_post = delete_post(data)

    if status_post['success'] == True:
        return status_post, 200
    
    return status_post, 401
