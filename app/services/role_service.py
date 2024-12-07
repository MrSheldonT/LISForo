from models import Role, User
from app import db

def generate_roles():
    try:
        admin_role = Role(name="admin")
        user_role = Role(name="user")

        db.session.add(admin_role)
        db.session.add(user_role)

        db.session.commit()

        print("Roles created successfully")
        return True
    except Exception as e:
        print(f"Error creating roles: {e}")
        return False

def get_users_by_rol(id_role):
    try:
        role = Role.query.get(id_role)
        if not role:
            print(f"Role with id {id_role} not found")
            return []
        return role.users

    except Exception as e:
        print(f"Error fetching users by role {e}")
        return None