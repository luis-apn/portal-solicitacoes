from datetime import datetime

from flask_login import UserMixin
from werkzeug.security import check_password_hash, generate_password_hash

from app.extensions import db

ROLE_SOLICITANTE = "SOLICITANTE"
ROLE_ATENDENTE = "ATENDENTE"


class User(UserMixin, db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), nullable=False, unique=True)
    password_hash = db.Column(db.String(255), nullable=False)
    full_name = db.Column(db.String(120), nullable=False)
    role = db.Column(db.Enum(ROLE_SOLICITANTE, ROLE_ATENDENTE), nullable=False, default=ROLE_SOLICITANTE)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.now)

    def set_password(self, password):
        # Guardamos apenas o hash da senha, nunca a senha em texto puro.
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def is_atendente(self):
        return self.role == ROLE_ATENDENTE

    def to_dict(self):
        # password_hash não é enviado para o frontend.
        return {
            "id": self.id,
            "username": self.username,
            "full_name": self.full_name,
            "role": self.role,
        }
