from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_cors import CORS
#from flask_restx import Api, Resource, fields

db = SQLAlchemy()
bcrypt = Bcrypt()
#api = Api()

def create_app():
    app = Flask(__name__)
    CORS(app, resources={r"/*": {"origins": "*"}})
    app.config.from_object("app.config.Config")
    
    db.init_app(app)
    bcrypt.init_app(app)
    #api.init_app(app)

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