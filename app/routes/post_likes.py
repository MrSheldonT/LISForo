from flask import Blueprint, request, jsonify
from app.services.post_like_service import like_post, remove_like_post, show_likes_by_post,show_likes_of_post_by_user

comment_likes_bp = Blueprint("comment_likes", __name__)

@comment_likes_bp.route("/like_post", methods=['POST'])
def like_post_data():
    data = request.json
    data['id_user'] = request.id_user
    if not data or 'id_user' not in data or 'id_post' not in data:
        return jsonify({'success': False, 'message': "Parameters not provided (id_post, id_user)"}), 400

    status_new_like  = like_post(data)
    if status_new_like['success'] == True:
        return status_new_like, 200
    
    return status_new_like, 401

@comment_likes_bp.route("/unlike_post", methods=['DELETE'])
def unlike_post_data():
    data = request.json
    data['id_user'] = request.id_user
    if not data or 'id_user' not in data or 'id_post_like' not in data:
        return jsonify({'success': False, 'message': "Parameters not provided (id_post_like, id_user)"}), 400
    
    status_unlike  = remove_like_post(data)
    if status_unlike['success'] == True:
        return status_unlike, 200
    
    return status_unlike, 401

@comment_likes_bp.route("/likes_by_post", methods=['GET'])
def likes_by_comment():
    id_post = request.args.get('id_post')

    if not id_post:
        return {"success": False, "message": "id_post is required"}, 400
    status_likes_by_comment = show_likes_by_post({'id_post': id_post})

    if status_likes_by_comment['success'] == True:
        return status_likes_by_comment, 200
    
    return status_likes_by_comment, 401

@comment_likes_bp.route("/likes_by_user", methods=['GET'])
def likes_by_user():

    if not request.id_user:
        return {"success": False, "message": "id_user is required"}, 400
    status_likes_by_comment = show_likes_of_post_by_user({'id_user': request.id_user})

    if status_likes_by_comment['success'] == True:
        return status_likes_by_comment, 200
    
    return status_likes_by_comment, 401