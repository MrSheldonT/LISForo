from flask import Blueprint, request, jsonify
from app.utils.token_management import token_required
from app.services.post_like_service import like_post, remove_like_post, show_likes_by_post,show_likes_of_post_by_user, is_liked_by_user

post_likes_bp = Blueprint("post_likes", __name__)

@post_likes_bp.route("/like_post", methods=['POST'])
@token_required
def like_post_data():
    data = request.json
    data['id_user'] = request.id_user
    if not data or 'id_user' not in data or 'id_post' not in data:
        return jsonify({'success': False, 'message': "Parameters not provided (id_post, id_user)"}), 400

    status_new_like  = like_post(data)
    if status_new_like['success'] == True:
        return status_new_like, 200
    
    return status_new_like, 401

@post_likes_bp.route("/unlike_post", methods=['DELETE'])
@token_required
def unlike_post_data():
    data = request.json
    data['id_user'] = request.id_user
    data['id_role'] = request.id_role
    
    if not data or 'id_user' not in data or 'id_post' not in data or 'id_role' not in data:
        return jsonify({'success': False, 'message': "Parameters not provided (id_post, id_user)"}), 400
    
    status_unlike  = remove_like_post(data)
    if status_unlike['success'] == True:
        return status_unlike, 200
    return status_unlike, 401

@post_likes_bp.route("/likes_by_post", methods=['GET'])
@token_required
def likes_by_comment():
    id_post = request.args.get('id_post')

    if not id_post:
        return {"success": False, "message": "id_post is required"}, 400
    status_likes_by_comment = show_likes_by_post({'id_post': id_post})

    if status_likes_by_comment['success'] == True:
        return status_likes_by_comment, 200
    
    return status_likes_by_comment, 401

@post_likes_bp.route("/likes_by_user", methods=['GET'])
@token_required
def likes_by_user():
    if not request.id_user:
        return {"success": False, "message": "id_user is required"}, 400
    status_likes_by_comment = show_likes_of_post_by_user({'id_user': request.id_user})

    if status_likes_by_comment['success'] == True:
        return status_likes_by_comment, 200
    
    return status_likes_by_comment, 401

@post_likes_bp.route("/is_liked", methods=['GET'])
@token_required
def is_liked():
    id_post = request.args.get('id_post')
    if not request.id_user or not id_post:
        return {"success": False, "message": "id_post is required"}, 400
    status_likes_by_comment = is_liked_by_user({'id_user': request.id_user, 'id_post': id_post})

    if status_likes_by_comment['success'] == True:
        return status_likes_by_comment, 200
    
    return status_likes_by_comment, 401

