from flask import Blueprint

def register_routes(app):
    from app.routes import posts, comments, users, roles
    app.register_blueprint(users.user_bp, url_prefix = "/users")
    app.register_blueprint(roles.roles_bp, url_prefix = "/roles")