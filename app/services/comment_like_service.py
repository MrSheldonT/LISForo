from app import db
from app.models import CommentLike, User, Role

def like_post(like_data):
    try:
        comment_like = CommentLike(
            id_comment = like_data['id_comment']
            , id_user = like_data['id_user']
        )

        db.session.add(comment_like)
        db.session.commit()

    except Exception as e:
        db.session.rollback()
        return {"success": False, "message": str(e)}
    
def show_like(comment_like: CommentLike): #devolver true o false
    try:
            user = User.query.get_or_404(comment_like.id_comment)
            return {
                 "id_comment_like": comment_like.id_comment_like
                 , "id_comment": comment_like.id_comment
                 , "id_post": comment_like.id_post
                 , "id_user": comment_like.id_comment
                 , "author": user.username
                 , "created_at": comment_like.created_at
            }
    except Exception as e:
        return {"success": False, "message": str(e)}

def show_likes_by_comment(comment_data):
    try:
        likes_from_comment = CommentLike.query.filter_by(id_comment=comment_data.get('id_comment')).all()
        like_datails = []

        for comment_like in likes_from_comment:
            like_datails.append(show_like(comment_like))
        
        return {"success": True, "like_datails": like_datails}, 

    except Exception as e:
        return {"success": False, "message": str(e)}

def show_likes_by_user(comment_data):
    try:
        likes_from_user = CommentLike.query.filter_by(id_comment=comment_data.get('id_user')).all()
        like_datails = []

        for comment_like in likes_from_user:
            like_datails.append(show_like(comment_like))
        
        return {"success": True, "like_datails": like_datails}, 

    except Exception as e:
        return {"success": False, "message": str(e)}
    
def remove_like(comment_like):
    try:

        if not 'id_comment_like' in comment_like:
            return {"success": False, "message": "The like you are trying to removed is not found"}
        
        comment_like = CommentLike.query.get_or_404(comment_like.get('id_comment_like'))
        role = Role.query.get_or_404(comment_like.get('id_role'))
 
        if comment_like.id_user == comment_like['id_user'] or role.name == 'admin':
            db.session.delete(comment_like)
            db.session.commit()
            return {"success": True, "message": "Like removed successfully"}
        
        return {"success": False, "message": "The like you are trying to removed is not yours"}
    
    except Exception as e:
        return {"success": False, "message": str(e)}