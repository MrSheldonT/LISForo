from flask import Blueprint, request, jsonify
from app import db
from app.models import User

user_bp = Blueprint("users", __name__)

@user_bp.route("/", methods=['POST'])
def register():
    data = request.json
    new_user = User(username=data['username'], email=data['email'], password=data['password'])
    db.session.add(new_user)
    db.session.commit()
    return jsonify({'message': 'User registered successfully'}), 201