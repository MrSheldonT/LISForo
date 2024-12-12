from flask import Blueprint, jsonify, request
from app.utils.token_management import token_required
from app.services.news_service import generate_post

bot_news_bp = Blueprint('bot_news', __name__)

@bot_news_bp.route("/generate_post", methods=['GET'])
def generate_post_data():
    return  generate_post()
    