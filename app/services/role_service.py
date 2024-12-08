from app.models import Role, User
from app import db

def get_users_by_rol(id_role):
    try:
        role = Role.query.get_or_404(id_role)
        users = [{"id_user": user.id_user, "username": user.username, "email": user.email} for user in role.users]

        return {"success": True, "message": "Roles created successfully", "users": users }

    except Exception as e:
        return {"success": False, "message": f"Error fetching users by role {e}"}