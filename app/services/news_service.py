import requests
from app import create_app, db
from app.models import Post, User
from app.services.user_service import create_user, login_user
from app.services.post_service import create_post
import os

app = create_app()


with app.app_context():
    bot_data = {
        'username': "NewsAPIbot"
        , 'email': "NewAPIBot@automate.api"
        , 'password': "This is 1 password secure;)"
    }

    user_bot = User.query.filter_by(username=bot_data['username']).first()
    if not user_bot:
        status_bot_user = create_user(bot_data)
        if not status_bot_user['success']:
            print(status_bot_user)
            exit(1) 

    user_bot = User.query.filter_by(username=bot_data['username']).first()

    if not user_bot:
        print({"success": False, "message": "Failed to fetch bot user after creation."})
        exit(1)

    bot_data['token'] = login_user(bot_data).get('token')
    if not bot_data['token']:
        print({"success": False, "message": "Failed to authenticate bot user."})
        exit(1)

    API_KEY = os.getenv('NEW_API_KEY', ':/')
    URL = 'https://newsapi.org/v2/top-headlines'
    params = {
        'apiKey': API_KEY
        , 'category': 'entertainment'
        , 'pageSize': 1
        , 'source': 'bbc-news'
    }
    response = requests.get(URL, params=params)

    data = response.json()
    if data['status'] == 'ok':
        for article in data['articles']:
            print(article)
            if not Post.query.filter_by(title=article['title']).first():
                status_new_post = create_post({
                    'title': article['title']
                    , 'content': f"{article['description']}\n\nLeer más: {article['url']}"
                    , 'id_user': user_bot.id_user
                })
                print(status_new_post)
        print({"success": True, "message": "Posts creados exitosamente."})
    else:
        print({"success": False, "message": data.get('message')})
