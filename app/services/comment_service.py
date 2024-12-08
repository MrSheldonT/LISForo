import markdown
from app.models import Comment, Role, User
from app import db

def create_comment(comment_data):
    try:
        new_comment = Comment(
            id_post = comment_data.get('id_post')
            , id_user = comment_data.get('id_user') # token required
            , content = comment_data.get('content')
        )
        db.session.add(new_comment)
        db.session.commit()
        return {"success": True, "message": "Comment created successfully"}

    except Exception as e:
        db.session.rollback()
        return {"success": False, "message": str(e)}

def show_comment(comment: Comment):
    try:
        user = User.query.get_or_404(comment.id_user)
        role = Role.query.get_or_404(user.id_role)
        html_content = markdown.markdown(comment.content)

        return {
            "id_comment": comment.id_comment
            , "id_user": user.id_user
            , "id_role": role.id_role
            , "role": role.name
            , "author": user.username
            , "content": html_content# comment.content
            , "created_at": comment.created_at
            , "updated_at": comment.updated_at
            , "is_edited": comment.is_edited
            , "id_post": comment.id_post
        }
    
    except Exception as e:
        return {"success": False, "message": str(e)}

def show_comments_by_user(user_data):
    try:
        comments = Comment.query.filter_by(id_user=user_data.get('id_user')).all()
        comments_details = []
        
        for comment in comments:
            comments_details.append(show_comment(comment))
        return {"success": True, "comment_details": comments_details}
    
    except Exception as e:
        return {"success": False, "message": str(e)}
    
def show_comments_by_post(post_data):
    try:
        comments = Comment.query.filter_by(id_post=post_data.get('id_post')).all()
        comments_details = []
        
        for comment in comments:
            comments_details.append(show_comment(comment))
        return {"success": True, "comment_details": comments_details}
    
    except Exception as e:
        return {"success": False, "message": str(e)}
    
def update_comment(comment_data):
    try:
        try:
            comment = Comment.query.get_or_404(comment_data.get('id_comment'))
        except Exception as e:
            return {"success": False, "message": "Comment not found"}

        if comment.id_user == comment_data['id_user']:
            comment.content = comment_data['content'] # add trigger database
            db.session.commit()
            return {"success": True, "message": "Comment updated successfully"}
        
        return {"success": False, "message": "You do not have sufficient privileges to perform this action"}
    
    except Exception as e:
        return {"success": False, "message": str(e)}
    
def delete_comment(comment_data):
    try:

        if not 'id_comment' in comment_data:
            return {"success": False, "message": "The comment you are trying to delete is not found"}
        
        try:
            comment = Comment.query.get_or_404(comment_data.get('id_comment'))
        except Exception as e:
            return {"success": False, "message": "Comment not found"}

        role = Role.query.get_or_404(comment_data.get('id_role'))
 
        if comment.id_user == comment_data['id_user'] or role.name == 'admin':
            db.session.delete(comment)
            db.session.commit()
            return {"success": True, "message": "Comment deleted successfully"}
        
        return {"success": False, "message": "You do not have sufficient privileges to perform this action"}
    
    except Exception as e:
        db.session.rollback()
        return {"success": False, "message": str(e)}

