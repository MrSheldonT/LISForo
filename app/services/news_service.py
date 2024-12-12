import requests
import random
from app import create_app, db
from app.models import Post, User
from app.services.user_service import create_user, login_user
from app.services.post_service import create_post
import os

def generate_post():
    bot_data = {
        'username': "NewsAPIbot🤖"
        , 'email': "NewAPIBot@automate.api"
        , 'password': "This is 1 secure password;)"
    }
    print("hola")
    user_bot = User.query.filter_by(username=bot_data['username']).first()
    if not user_bot:
        status_bot_user = create_user(bot_data)
        if not status_bot_user['success']:
            return {status_bot_user}
             

    user_bot = User.query.filter_by(username=bot_data['username']).first()

    if not user_bot:
        return {"success": False, "message": "Failed to fetch bot user after creation."}

    bot_data['token'] = login_user(bot_data).get('token')
    if not bot_data['token']:
        return {"success": False, "message": "Failed to authenticate bot user."}

    API_KEY = os.getenv('NEW_API_KEY', ':/')
    URL = 'https://newsapi.org/v2/top-headlines'
    params = {
        'apiKey': API_KEY
        , 'category': random.choice(['business', 'entertainment','general','health','sciences','ports','technology'])
        , 'pageSize': 1
    }
    response = requests.get(URL, params=params)
    data = response.json()
    if data['status'] == 'ok':
        for article in data['articles']:
            if not Post.query.filter_by(title=article['title']).first():
                if not article['description']:
                    article['description'] = "No se adjuntó descripción para esta noticia"
                status_new_post = create_post({
                    'title': article['title']
                    , 'content': f"{article['description']}\n\n Entérate de la noticia más a detalle: [URL]({article['url']})" + (f"\n\n![Imagen relacionada]({article['urlToImage']})" if 'urlToImage' in article and article['urlToImage'] else "")
                    , 'id_user': user_bot.id_user
                })
                print(status_new_post)
        db.session.commit()
        return {"success": True, "message": "Posts creados exitosamente."}
    else:
        return {"success": False, "message": data.get('message')}
