from app import db
from app.models import PostLike, User, Role
from werkzeug.exceptions import NotFound

def like_post(like_data):
    try:

        if PostLike.query.filter_by(id_post=like_data['id_post'], id_user=like_data['id_user']).first():
            return {"success": False, "message": "Like already exists"}
        
        post_like = PostLike(
            id_post = like_data['id_post']
            , id_user = like_data['id_user']
        )
        
        db.session.add(post_like)
        db.session.commit()
        return {"success": True, "message": "Like"}

    except Exception as e:
        db.session.rollback()
        return {"success": False, "message": str(e)}
    
def show_like_post(post_like: PostLike): 
    try:
            user = User.query.get_or_404(post_like.id_user)
            return {
                 "id_post_like": post_like.id_post_like                 
                 , "id_post": post_like.id_post
                 , "id_user": post_like.id_user
                 , "author": user.username
                 , "created_at": post_like.created_at
            }
    except Exception as e:
        return {"success": False, "message": str(e)}

def show_likes_by_post(post_data):
    try:
        likes_from_post = PostLike.query.filter_by(id_post=post_data.get('id_post')).all()
        like_details = []

        for post_like in likes_from_post:
            like_details.append(show_like_post(post_like))
        
        return {"success": True, "like_details": like_details, 'like_counter': len(like_details)}

    except Exception as e:
        return {"success": False, "message": str(e)}

def show_likes_of_post_by_user(comment_data):
    try:
        likes_from_user = PostLike.query.filter_by(id_user=comment_data.get('id_user')).all()
        like_details = []

        for post_like in likes_from_user:
            like_details.append(show_like_post(post_like))
        
        return {"success": True, "like_details": like_details, 'like_counter': len(like_details)} 

    except Exception as e:
        return {"success": False, "message": str(e)}
    
def is_liked_by_user(post_like):
    try:
        post_like_instance = PostLike.query.filter_by(id_post=post_like.get('id_post'), id_user=post_like.get('id_user')).first()
        if post_like_instance:
            return {"success": True, 'message': "Like", 'isLiked': True } 
        return {"success": True, 'message': "No Like", 'isLiked': False } 
    except Exception as e:
        return {"success": False, "message": str(e), 'isLiked': False}
    
def remove_like_post(post_like):
    try:
        post_like_instance = PostLike.query.filter_by(id_post=post_like.get('id_post'), id_user=post_like.get('id_user')).first()
        
        if not post_like_instance:
            return {'success': False, 'message': "The like does not belong to any record, please try again"}

        role = Role.query.get_or_404(post_like.get('id_role'))

        if post_like_instance.id_user == post_like['id_user'] or role.name == 'admin':
            db.session.delete(post_like_instance)
            db.session.commit() 
            return {"success": True, "message": "Like removed successfully"}
        
        return {"success": False, "message": "The like you are trying to remove is not yours or you do not have privileges"}

    except Exception as e:
        return {"success": False, "message": str(e)}
