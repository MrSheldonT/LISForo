from flask import Blueprint

def register_routes(app):
    from app.routes import posts, comments, users, roles, comment_likes, bot_news, post_likes
    app.register_blueprint(users.user_bp, url_prefix="/users")
    app.register_blueprint(roles.roles_bp, url_prefix="/roles")
    app.register_blueprint(posts.post_bp, url_prefix="/posts" )
    app.register_blueprint(post_likes.post_likes_bp, url_prefix="/post_likes")
    app.register_blueprint(comments.comments_bp, url_prefix="/comments")
    app.register_blueprint(comment_likes.comment_likes_bp, url_perfix="/likes")
    app.register_blueprint(bot_news.bot_news_bp, url_prefix = "/bot")