import pytest

from app import create_app
from app.config import TestConfig
from app.extensions import db
from app.models import ROLE_ATENDENTE, ROLE_SOLICITANTE, Category, User

PASSWORD = "senha123"


@pytest.fixture()
def app():
    """Cria um app com banco SQLite em memória, novo para cada teste."""
    app = create_app(TestConfig)

    with app.app_context():
        db.create_all()
        db.session.add_all([Category(name="TI"), Category(name="RH"), Category(name="Compras")])
        for username, role in [("ana", ROLE_SOLICITANTE), ("beto", ROLE_SOLICITANTE), ("carla", ROLE_ATENDENTE)]:
            user = User(username=username, full_name=username.title(), role=role)
            user.set_password(PASSWORD)
            db.session.add(user)
        db.session.commit()

    yield app

    with app.app_context():
        db.drop_all()


@pytest.fixture()
def login_as(app):
    """Retorna um cliente de teste já logado com o usuário informado."""

    def _login_as(username):
        client = app.test_client()
        response = client.post("/api/auth/login", json={"username": username, "password": PASSWORD})
        assert response.status_code == 200
        return client

    return _login_as


VALID_REQUEST = {
    "title": "Notebook com defeito",
    "description": "A tela do notebook não liga mais.",
    "category_id": 1,
}
