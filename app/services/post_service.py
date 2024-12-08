from app.models import Post, User, Role
from app import db
import markdown

def create_post(post_data):
    try:
        new_post = Post(
            id_user = post_data.get('id_user')
            , title = post_data.get('title')
            , content = post_data.get('content')    
        )
        print(new_post.__getstate__)
        db.session.add(new_post)
        db.session.commit()
        
        return {"success": True, "message": "Post created successfully"}
    
    except Exception as e:
        db.session.rollback()
        return {"success": False, "message": str(e)}
    
def show_post(post_data):
    try:
        try:
            post = Post.query.get_or_404(post_data.get('id_post'))
        except Exception as e:
            return {"success": False, "message": "Post not found"}
        
        user = User.query.get_or_404(post.id_user)
        html_content = markdown.markdown(post.content)

        post_details = {
            "id_post": post.id_post
            ,  "id_user": user.id_user
            , "author": user.username
            , "title": post.title
            , "content": html_content# post.content
            , "created_at": post.created_at
        }
        return {"success": True, "message": "Post consulted successfully", "post" : post_details}
    
    except Exception as e:
        return {"success": False, "message": str(e)}

def update_post(post_data):
    try:
        try:
            post = Post.query.get_or_404(post_data.get('id_post'))
        except Exception as e:
            return {"success": False, "message": "Post not found"}
        
        role = Role.query.get_or_404(post_data.get('id_role'))
        
        if post.id_user == post_data['id_user'] or role.name == 'admin':
            if 'title' in post_data:
                post.title = post_data['title']
            if 'content' in post_data:
                post.content = post_data['content']
            db.session.commit()
            return {"success": True, "message": "Post updated successfully"}
        
        return {"success": False, "message": "You do not have sufficient privileges to perform this action"}
    
    except Exception as e:
        db.session.rollback()
        return {"success": False, "message": str(e)}
    
def delete_post(post_data):
    try:
        try:
            post = Post.query.get_or_404(post_data.get('id_post'))
        except Exception as e:
            return {"success": False, "message": "Post not found"}
        
        post = Post.query.get_or_404(post_data.get('id_post'))
        role = Role.query.get_or_404(post_data.get('id_role'))
        
        if post.id_user == post_data['id_user'] or role.name == 'admin':
            db.session.delete(post)
            db.session.commit()
            return {"success": True, "message": "Post deleted successfully"}
        
        return {"success": False, "message": "You do not have sufficient privileges to perform this action"}
    
    except Exception as e:
        db.session.rollback()
        return {"success": False, "message": str(e)}