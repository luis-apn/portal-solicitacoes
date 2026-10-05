from flask import Blueprint, jsonify
from flask_login import login_required

from app.services import request_service

dashboard_bp = Blueprint("dashboard", __name__, url_prefix="/api/dashboard")


@dashboard_bp.get("")
@login_required
def dashboard():
    return jsonify(request_service.get_dashboard())
