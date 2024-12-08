from app import create_app
from app.services.news_service import fetch_and_create_posts

app = create_app()

with app.app_context():
    result = fetch_and_create_posts()
    print(result)
