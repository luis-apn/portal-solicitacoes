from flask import Flask, jsonify

from app.config import Config
from app.errors import register_error_handlers
from app.extensions import cors, db, login_manager


def create_app(config_class=Config):
    """Cria e configura a aplicação Flask (padrão Application Factory)."""
    app = Flask(__name__)
    app.config.from_object(config_class)

    db.init_app(app)
    login_manager.init_app(app)
    cors.init_app(
        app,
        resources={r"/api/*": {"origins": app.config["CORS_ORIGINS"]}},
        supports_credentials=True,
    )

    from app.models import User

    @login_manager.user_loader
    def load_user(user_id):
        # O Flask-Login guarda só o id do usuário no cookie de sessão.
        # A cada requisição ele chama esta função para buscar o usuário no banco.
        return db.session.get(User, int(user_id))

    @login_manager.unauthorized_handler
    def unauthorized():
        # Por padrão o Flask-Login redireciona para uma página HTML de login.
        # Como somos uma API, devolvemos 401 em JSON.
        return jsonify({"error": "Você precisa estar logado."}), 401

    from app.routes.auth import auth_bp
    from app.routes.categories import categories_bp
    from app.routes.dashboard import dashboard_bp
    from app.routes.requests import requests_bp

    app.register_blueprint(auth_bp)
    app.register_blueprint(requests_bp)
    app.register_blueprint(categories_bp)
    app.register_blueprint(dashboard_bp)

    register_error_handlers(app)

    return app
