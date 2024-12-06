from flask import Blueprint, jsonify
from app import db
from app.models import Role

roles_bp = Blueprint('roles', __name__)

@roles_bp.route('/',methods=['GET'])
def setRoles():
    admin = Role(name="admin")
    user = Role(name="user")
    db.session.add(admin)
    db.session.add(user)
    db.session.commit()
    return jsonify({"message": "The roles is uploaded"})