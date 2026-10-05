from datetime import datetime

from app.extensions import db

STATUS_ABERTO = "ABERTO"
STATUS_EM_ATENDIMENTO = "EM_ATENDIMENTO"
STATUS_CONCLUIDO = "CONCLUIDO"
STATUSES = [STATUS_ABERTO, STATUS_EM_ATENDIMENTO, STATUS_CONCLUIDO]


class ServiceRequest(db.Model):
    # A classe não se chama "Request" para não confundir com o flask.request.
    __tablename__ = "requests"

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(150), nullable=False)
    description = db.Column(db.Text, nullable=False)
    requester_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    category_id = db.Column(db.Integer, db.ForeignKey("categories.id"), nullable=False)
    status = db.Column(db.Enum(*STATUSES), nullable=False, default=STATUS_ABERTO)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.now)
    updated_at = db.Column(db.DateTime, nullable=False, default=datetime.now, onupdate=datetime.now)

    # relationship permite acessar request.category.name e request.requester.full_name
    requester = db.relationship("User")
    category = db.relationship("Category")

    def to_dict(self):
        return {
            "id": self.id,
            "title": self.title,
            "description": self.description,
            "category_id": self.category_id,
            "category": self.category.name,
            "requester_id": self.requester_id,
            "requester": self.requester.full_name,
            "status": self.status,
            "created_at": self.created_at.isoformat(timespec="seconds"),
            "updated_at": self.updated_at.isoformat(timespec="seconds"),
        }
