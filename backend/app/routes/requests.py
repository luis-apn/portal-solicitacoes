from flask import Blueprint, jsonify, request
from flask_login import current_user, login_required

from app.services import request_service
from app.validators import get_json_body, parse_filters, validate_request_data, validate_status

requests_bp = Blueprint("requests", __name__, url_prefix="/api/requests")


@requests_bp.get("")
@login_required
def list_requests():
    filters = parse_filters(request.args)
    items = request_service.list_requests(filters)
    return jsonify({"items": [item.to_dict() for item in items]})


@requests_bp.post("")
@login_required
def create_request():
    data = validate_request_data(get_json_body())
    service_request = request_service.create_request(current_user, data)
    return jsonify({"request": service_request.to_dict()}), 201


@requests_bp.get("/<int:request_id>")
@login_required
def get_request(request_id):
    service_request = request_service.get_request(request_id)
    return jsonify({"request": service_request.to_dict()})


@requests_bp.put("/<int:request_id>")
@login_required
def update_request(request_id):
    data = validate_request_data(get_json_body())
    service_request = request_service.update_request(current_user, request_id, data)
    return jsonify({"request": service_request.to_dict()})


@requests_bp.delete("/<int:request_id>")
@login_required
def delete_request(request_id):
    request_service.delete_request(current_user, request_id)
    return jsonify({"message": "Solicitação excluída."})


@requests_bp.patch("/<int:request_id>/status")
@login_required
def change_status(request_id):
    new_status = validate_status(get_json_body())
    service_request = request_service.change_status(current_user, request_id, new_status)
    return jsonify({"request": service_request.to_dict()})
