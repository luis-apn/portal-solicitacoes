"""Validação dos dados que chegam do frontend.

Nunca confiamos no que vem do cliente: tudo é conferido aqui antes de chegar
nas regras de negócio.
"""
from datetime import datetime

from flask import request

from app.errors import AppError
from app.models import STATUSES


def get_json_body():
    """Lê o corpo JSON da requisição. Se não for JSON válido, retorna erro 400."""
    data = request.get_json(silent=True)
    if not isinstance(data, dict):
        raise AppError("O corpo da requisição deve ser um JSON válido.")
    return data


def validate_login_data(data):
    username = str(data.get("username") or "").strip()
    password = str(data.get("password") or "")

    errors = {}
    if not username:
        errors["username"] = "Informe o usuário."
    if not password:
        errors["password"] = "Informe a senha."
    if errors:
        raise AppError("Dados inválidos.", 400, errors)

    return username, password


def validate_request_data(data):
    """Valida os campos de criação/edição de uma solicitação."""
    title = str(data.get("title") or "").strip()
    description = str(data.get("description") or "").strip()
    category_id = data.get("category_id")

    errors = {}
    if len(title) < 3 or len(title) > 150:
        errors["title"] = "O título deve ter entre 3 e 150 caracteres."
    if len(description) < 10 or len(description) > 5000:
        errors["description"] = "A descrição deve ter entre 10 e 5000 caracteres."
    try:
        category_id = int(category_id)
    except (TypeError, ValueError):
        errors["category_id"] = "Selecione uma categoria."

    if errors:
        raise AppError("Dados inválidos.", 400, errors)

    return {"title": title, "description": description, "category_id": category_id}


def validate_status(data):
    status = data.get("status")
    if status not in STATUSES:
        raise AppError("Status inválido.", 400, {"status": "Valores aceitos: " + ", ".join(STATUSES)})
    return status


def _parse_date(value, field):
    try:
        return datetime.strptime(value, "%Y-%m-%d").date()
    except ValueError:
        raise AppError("Filtro inválido.", 400, {field: "Use o formato AAAA-MM-DD."})


def parse_filters(args):
    """Lê os filtros da URL (?q=...&status=...&category_id=...&date_from=...&date_to=...)."""
    filters = {}

    if args.get("q"):
        filters["q"] = args["q"].strip()

    if args.get("status"):
        if args["status"] not in STATUSES:
            raise AppError("Filtro inválido.", 400, {"status": "Status inválido."})
        filters["status"] = args["status"]

    if args.get("category_id"):
        try:
            filters["category_id"] = int(args["category_id"])
        except ValueError:
            raise AppError("Filtro inválido.", 400, {"category_id": "Categoria inválida."})

    if args.get("date_from"):
        filters["date_from"] = _parse_date(args["date_from"], "date_from")
    if args.get("date_to"):
        filters["date_to"] = _parse_date(args["date_to"], "date_to")

    if "date_from" in filters and "date_to" in filters:
        if filters["date_from"] > filters["date_to"]:
            raise AppError("Filtro inválido.", 400, {"date_from": "A data inicial deve ser menor que a final."})

    return filters
