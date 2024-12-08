from flask import Blueprint, request, jsonify
from app.services.comment_like_service import like_post, remove_like, show_likes_by_comment

comment_likes_bp = Blueprint("comment_likes", __name__)

@comment_likes_bp.route("/like_post", methods=['POST'])
def like_post_data():
    data = request.json
    data['id_user'] = request.id_user
    if not data or 'id_user' not in data or 'id_comment' not in data:
        return jsonify({'success': False, 'message': "Parameters not provided (id_comment, id_user)"}), 400

    status_new_like  = like_post(data)
    if status_new_like['success'] == True:
        return status_new_like, 200
    
    return status_new_like, 401

@comment_likes_bp.route("/unlike_post", methods=['DELETE'])
def unlike_post_data():
    data = request.json
    data['id_user'] = request.id_user
    if not data or 'id_user' not in data or 'id_comment_like' not in data:
        return jsonify({'success': False, 'message': "Parameters not provided (id_comment_like, id_user)"}), 400
    
    status_unlike  = remove_like(data)
    if status_unlike['success'] == True:
        return status_unlike, 200
    
    return status_unlike, 401

@comment_likes_bp.route("/likes_by_comment", methods=['GET'])
def likes_by_comment():
    id_comment = request.args.get('id_comment')

    if not id_comment:
        return {"success": False, "message": "id_comment is required"}, 400
    status_likes_by_comment = show_likes_by_comment({'id_comment': id_comment})

    if status_likes_by_comment['success'] == True:
        return status_likes_by_comment, 200
    
    return status_likes_by_comment, 401

@comment_likes_bp.route("/likes_by_user", methods=['GET'])
def likes_by_user():

    if not request.id_user:
        return {"success": False, "message": "id_comment is required"}, 400
    status_likes_by_comment = show_likes_by_comment({'id_comment': request.id_user})

    if status_likes_by_comment['success'] == True:
        return status_likes_by_comment, 200
    
    return status_likes_by_comment, 401