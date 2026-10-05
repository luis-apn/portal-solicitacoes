from flask import Blueprint, jsonify
from flask_login import current_user, login_required, login_user, logout_user

from app.services import auth_service
from app.validators import get_json_body, validate_login_data

auth_bp = Blueprint("auth", __name__, url_prefix="/api/auth")


@auth_bp.post("/login")
def login():
    username, password = validate_login_data(get_json_body())
    user = auth_service.authenticate(username, password)
    login_user(user)  # cria a sessão (cookie assinado com o SECRET_KEY)
    return jsonify({"user": user.to_dict()})


@auth_bp.post("/logout")
@login_required
def logout():
    logout_user()
    return jsonify({"message": "Logout realizado."})


@auth_bp.get("/me")
@login_required
def me():
    # Usado pelo frontend para saber se ainda existe uma sessão ativa.
    return jsonify({"user": current_user.to_dict()})
