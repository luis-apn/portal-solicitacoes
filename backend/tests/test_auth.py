from tests.conftest import PASSWORD


def test_login_com_sucesso(app):
    client = app.test_client()
    response = client.post("/api/auth/login", json={"username": "ana", "password": PASSWORD})

    assert response.status_code == 200
    assert response.get_json()["user"]["username"] == "ana"
    assert "password_hash" not in response.get_json()["user"]


def test_login_com_senha_errada(app):
    client = app.test_client()
    response = client.post("/api/auth/login", json={"username": "ana", "password": "errada"})

    assert response.status_code == 401


def test_login_sem_campos(app):
    client = app.test_client()
    response = client.post("/api/auth/login", json={})

    assert response.status_code == 400
    assert "username" in response.get_json()["details"]


def test_rotas_protegidas_sem_login(app):
    client = app.test_client()

    assert client.get("/api/requests").status_code == 401
    assert client.get("/api/dashboard").status_code == 401
    assert client.get("/api/categories").status_code == 401


def test_logout(login_as):
    client = login_as("ana")

    assert client.get("/api/auth/me").status_code == 200
    assert client.post("/api/auth/logout").status_code == 200
    assert client.get("/api/auth/me").status_code == 401
