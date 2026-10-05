"""Regras de negócio das solicitações.

Regras:
- Toda solicitação nasce com status ABERTO e com o usuário logado como solicitante.
- Só o próprio solicitante pode editar ou excluir, e só enquanto estiver ABERTO.
- Só usuários ATENDENTE podem alterar o status.
- O status segue a ordem: ABERTO -> EM_ATENDIMENTO -> CONCLUIDO.
"""
from datetime import datetime, time, timedelta

from app.errors import AppError
from app.extensions import db
from app.models import (
    STATUS_ABERTO,
    STATUS_CONCLUIDO,
    STATUS_EM_ATENDIMENTO,
    Category,
    ServiceRequest,
)

# Para cada status, qual é o próximo permitido.
NEXT_STATUS = {
    STATUS_ABERTO: STATUS_EM_ATENDIMENTO,
    STATUS_EM_ATENDIMENTO: STATUS_CONCLUIDO,
}


def list_requests(filters):
    query = ServiceRequest.query

    if "q" in filters:
        query = query.filter(ServiceRequest.title.ilike(f"%{filters['q']}%"))
    if "status" in filters:
        query = query.filter(ServiceRequest.status == filters["status"])
    if "category_id" in filters:
        query = query.filter(ServiceRequest.category_id == filters["category_id"])
    if "date_from" in filters:
        start = datetime.combine(filters["date_from"], time.min)
        query = query.filter(ServiceRequest.created_at >= start)
    if "date_to" in filters:
        # Menor que o dia seguinte às 00:00, para incluir o último dia inteiro.
        end = datetime.combine(filters["date_to"], time.min) + timedelta(days=1)
        query = query.filter(ServiceRequest.created_at < end)

    return query.order_by(ServiceRequest.created_at.desc(), ServiceRequest.id.desc()).all()


def get_request(request_id):
    service_request = db.session.get(ServiceRequest, request_id)
    if service_request is None:
        raise AppError("Solicitação não encontrada.", 404)
    return service_request


def _check_category(category_id):
    if db.session.get(Category, category_id) is None:
        raise AppError("Dados inválidos.", 400, {"category_id": "Categoria não encontrada."})


def _check_can_change(user, service_request, action):
    """Só o dono pode editar/excluir, e só se ainda estiver ABERTO."""
    if service_request.requester_id != user.id:
        raise AppError(f"Apenas o solicitante pode {action} esta solicitação.", 403)
    if service_request.status != STATUS_ABERTO:
        raise AppError(f"Só é possível {action} solicitações com status Aberto.", 409)


def create_request(user, data):
    _check_category(data["category_id"])

    service_request = ServiceRequest(
        title=data["title"],
        description=data["description"],
        category_id=data["category_id"],
        requester_id=user.id,
        status=STATUS_ABERTO,
    )
    db.session.add(service_request)
    db.session.commit()
    return service_request


def update_request(user, request_id, data):
    service_request = get_request(request_id)
    _check_can_change(user, service_request, "editar")
    _check_category(data["category_id"])

    service_request.title = data["title"]
    service_request.description = data["description"]
    service_request.category_id = data["category_id"]
    db.session.commit()
    return service_request


def delete_request(user, request_id):
    service_request = get_request(request_id)
    _check_can_change(user, service_request, "excluir")

    db.session.delete(service_request)
    db.session.commit()


def change_status(user, request_id, new_status):
    service_request = get_request(request_id)

    if not user.is_atendente():
        raise AppError("Apenas atendentes podem alterar o status.", 403)

    if NEXT_STATUS.get(service_request.status) != new_status:
        raise AppError(
            f"Não é possível mudar de {service_request.status} para {new_status}. "
            "A ordem é ABERTO -> EM_ATENDIMENTO -> CONCLUIDO.",
            409,
        )

    service_request.status = new_status
    db.session.commit()
    return service_request


def get_dashboard():
    return {
        "total": ServiceRequest.query.count(),
        "aberto": ServiceRequest.query.filter_by(status=STATUS_ABERTO).count(),
        "em_atendimento": ServiceRequest.query.filter_by(status=STATUS_EM_ATENDIMENTO).count(),
        "concluido": ServiceRequest.query.filter_by(status=STATUS_CONCLUIDO).count(),
    }


def list_categories():
    return Category.query.order_by(Category.name).all()
