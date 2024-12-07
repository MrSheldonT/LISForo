from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt


db = SQLAlchemy()
bcrypt = Bcrypt()
def create_app():
    app = Flask(__name__)
    app.config.from_object("app.config.Config")
    
    db.init_app(app)
    bcrypt.init_app(app)

    from app.routes import register_routes
    register_routes(app=app)

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