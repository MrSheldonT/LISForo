from app.models import User, Role
from app import db
from app.utils.user_data import valid_date, valid_email, valid_password, valid_username, encrypt_password, check_password
from app.utils.token_management import create_jwt_token
from werkzeug.exceptions import NotFound

def create_user(user_data):
    try:

        if not valid_username(user_data.get('username', '')):
            return {'success': False, 'message': "Invalid username"}

        password_valid, password_message = valid_password(user_data.get('password', ''))
        if not password_valid:
            return {'success': False, 'message': password_message}

        if not valid_email(user_data.get('email', '')):
            return {'success': False, 'message': "The email is invalid"}        
          
        role = Role.query.filter_by(name='user').first()
       
        if not role:
            return {'success': False, 'message': "Rol user is not exists"}
        
        exists_user_username = User.query.filter_by(username = user_data.get('username')).first()
        exists_user_email = User.query.filter_by(email = user_data.get('email')).first()

        if exists_user_username:
            return {'success': False, 'message': "The user you are trying to register already exists"}
        
        if exists_user_email:
            return {'success': False, 'message': "The email you are trying to register already exists"}
     
        new_user = User(
            username = user_data['username']
            , password = encrypt_password(user_data['password'])
            , email = user_data['email']
            , id_role=role.id_role
        )   
        db.session.add(new_user)
        db.session.commit()
        return {'success': True, 'message': "User register succesfully"}
    
    except Exception as e:
        db.session.rollback()
        return {'success': False, 'message': str(e)}

def show_user(user_data):
    try:
        user = User.query.get_or_404(user_data.get('id_user'))
        role = Role.query.get_or_404(user.id_role)
        return {'success': True, 'username' : user.username, 'email': user.email, 'role': role.name}
    
    except NotFound as e:
        return {'success': False, 'message': "The user id does not belong to any record, please try again"}
    except Exception as e:
        return {'success': False, 'message': str(e)}
    
def login_user(user_data):
    try:
        user = User.query.filter_by(username=user_data.get('username')).first()
        if not user:
            return {"success": False, "message": "The user does not exist"}
        
        if user and check_password(user_data.get('password'), user.password):
            token = create_jwt_token(user.id_user, user.id_role)
            return {"success": True, "message": "Login successful", "token":token}
        else:
            return {'success': True, 'message': "The password is incorrect"}
    
    except NotFound as e:
        return {'success': False, 'message': f"User with username {user_data.get('username')} was not found."}
    except Exception as e:
        return {'success': False, 'message': str(e)}

def update_user(user_data):
    try:
        user_account = User.query.get_or_404(user_data.get('id_user_account'))
        user_request = User.query.get_or_404(user_data.get('id_user_request'))
        role = Role.query.get_or_404(user_request.id_role)
        if not user_account:
            return {'success': False, 'message': "User not found"}

        if user_data.get('id_user_account') != user_data.get('id_user_request') and role.name != 'admin':
            return {'success': False, 'message': "The user is not you or does not have sufficient privileges"}

        if 'id_role' in user_data:
            if user_account.id_role == user_request.id_role:
                return {'success': False, 'message': "Cannot change the role to another administrator"} 
            user_account.id_role  = role.id_role
            db.session.commit()
            return {'success': True, 'message': "Role changed successfully"} 

        if 'password' in user_data:
            password_valid, password_message = valid_password(user_data.get('password', ''))
            if password_valid:
                user_account.password = encrypt_password(user_data['password'])
                db.session.commit()
                return {'success': True, 'message': "Password changed successfully "} 
            else:
               return {'success': False, 'message': password_message} 
        
        if 'username' in user_data:
            user_account.username = user_data['username']
            db.session.commit()
            return {'success': True, 'message': "Username changed successfully "} 
        
        if 'email' in user_data:
            user_account.email = user_data['email']
            return {'success': True, 'message': "Email changed successfully "} 

        return {'success': False, 'message': "Forgot to provide the parameter to change"}
    
    except Exception as e:
        db.session.rollback()
        return {'success': False, 'message': str(e)}