from app.models import User, Role
from app import db
from app.utils.user_data import valid_date, valid_email, valid_password, valid_username, encrypt_password, check_password
from app.utils.token_management import create_jwt_token, token_required

def create_user(user_data):
    try:

        if not valid_username(user_data.get('username', '')):
            return {"success": False, "message": "Invalid username"}

        password_valid, password_message = valid_password(user_data.get('password', ''))
        if not password_valid:
            return {"success": False, "message": password_message}

        if not valid_email(user_data.get('email', '')):
            return {"success": False, "message": "The email is not valid"}
        
        role = Role.query.filter_by(name='user').first()
       
        if not role:
            return {"success": False, "message": "The role does not exist"}
     
        new_user = User(
            username = user_data['username']
            , password = encrypt_password(user_data['password'])
            , email = user_data['email']
            , id_role=role.id_role
        )

        db.session.add(new_user)
        db.session.commit()
        return {"success": True, "message": "User registred succesfully"}
    
    except Exception as e:
        db.session.rollback()
        return {"success": False, "message": str(e)}

def show_user(user_data):
    try:
        user = User.query.filter_by(id_user=user_data.get('id_user')).first()
        role = Role.query.filter_by(id_role=user_data.get('id_role')).first()
        return {"success": True, "username": user.username, "email": user.email, "role": role.name}
    except Exception as e:
        return {"success": False, "message": str(e)}
    
def login_user(user_data):
    try:
        user = User.query.filter_by(username=user_data.get('username')).first()
        if not user:
            return {"success": False, "message": "The user does not exist"}
        
        if user and check_password(user_data.get('password'), user.password):
            token = create_jwt_token(user.id_user, user.id_role)
            return {"success": True, "message": "Login successful", "token":token}
        else:
            return {"success": True, "message": "The password is incorrect"}
    except Exception as e:
        return {"success": False, "message": str(e)}

def update_user(user_data):
    try:
        user = User.query.filter_by(id_user=user_data.get('id_user')).first()
        if not user:
            return {"success": False, "message": "User not found"}
    
        if 'password' in user_data:
            password_valid, password_message = valid_password(user_data.get('password', ''))
            if password_valid:
                user.password = encrypt_password(user_data['password'])
            else:
               return {"success": False, "message": password_message} 

        if 'username' in user_data:
            user.username = user_data['username']
        
        if 'email' in user_data:
            user.email = user_data['email']

        db.session.commit()
        return {"success": True, "message": "User updated successfully"}
    
    except Exception as e:
        db.session.rollback()
        return {"success": False, "message": str(e)}
    