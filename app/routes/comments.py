from flask import Blueprint, request, jsonify
from app.utils.token_management import token_required
from app.services.comment_service import create_comment, show_comment, update_comment, delete_comment, show_comments_by_user, show_comments_by_post

comments_bp = Blueprint('comments', __name__)

@comments_bp.route('/publish_comment', methods=['POST'])
@token_required
def publish_comment():
    data = request.json
    data['id_user'] = request.id_user

    new_comment = create_comment(data)
    if new_comment['success'] == True:
        return new_comment, 200
    
    return new_comment, 401
    
@comments_bp.route('/edit_comment', methods=['PATCH'])
@token_required
def edit_comment():
    data = request.json
    status_comments = update_comment(data)

    if status_comments['success'] == True:
        return status_comments, 200
    return status_comments, 400

@comments_bp.route('/delete_comment', methods=['DELETE'])
@token_required
def delete_comment_data():
    data = request.json
    data['id_user'] = request.id_user
    data['id_role'] = request.id_role
    status_comments = delete_comment(data)

    if status_comments['success'] == True:
        return status_comments, 200
    return status_comments, 400
@comments_bp.route('/comments_by_user', methods=['GET'])
@token_required
def comment_by_user():
    status_comments = show_comments_by_user({'id_user':request.id_user})

    if status_comments['success'] == True:
        return status_comments, 200
    return status_comments, 400
    
@comments_bp.route('/comments_by_post', methods=['GET'])
@token_required
def comments_by_post():
    data = request.json
    status_comments = show_comments_by_post(data)

    if status_comments['success'] == True:
        return status_comments, 200
    return status_comments, 400