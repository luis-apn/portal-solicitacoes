from flask import Blueprint, jsonify
from flask_login import login_required

from app.services import request_service

categories_bp = Blueprint("categories", __name__, url_prefix="/api/categories")


@categories_bp.get("")
@login_required
def list_categories():
    categories = request_service.list_categories()
    return jsonify({"items": [category.to_dict() for category in categories]})
