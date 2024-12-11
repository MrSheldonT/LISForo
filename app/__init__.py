from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_cors import CORS

db = SQLAlchemy()
bcrypt = Bcrypt()
def create_app():
    app = Flask(__name__)
    CORS(app, resources={r"/*": {"origins": "*"}})
    app.config.from_object("app.config.Config")
    
    db.init_app(app)
    bcrypt.init_app(app)

    from app.routes import register_routes
    #register_routes(app=app)
    from app.routes import posts, comments, users, roles, comment_likes
    app.register_blueprint(users.user_bp, url_prefix="/users")
    app.register_blueprint(roles.roles_bp, url_prefix="/roles")
    app.register_blueprint(posts.post_bp, url_prefix="/posts" )
    app.register_blueprint(comments.comments_bp, url_prefix="/comments")
    app.register_blueprint(comment_likes.comment_likes_bp, url_perfix="/likes")

    # checar lo de migrate

    @app.route("/")
    def index():
        return "Hello :D"

    @app.errorhandler(404)
    def page_404(e):
            return """
    <pre>
    ▐ ▄       ▄▄▄▄▄    ·▄▄▄      ▄• ▄▌ ▐ ▄ ·▄▄▄▄
    •█▌▐█▪     •██      ▐▄▄·▪     █▪██▌•█▌▐███▪ ██
    ▐█▐▐▌ ▄█▀▄  ▐█.▪    ██▪  ▄█▀▄ █▌▐█▌▐█▐▐▌▐█· ▐█▌
    ██▐█▌▐█▌.▐▌ ▐█▌·    ██▌.▐█▌.▐▌▐█▄█▌██▐█▌██. ██
    ▀▀ █▪ ▀█▄▀▪ ▀▀▀     ▀▀▀  ▀█▄▀▪ ▀▀▀ ▀▀ █▪▀▀▀▀▀•
    </pre>
            """, 404

    return app 