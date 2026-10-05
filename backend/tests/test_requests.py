from tests.conftest import VALID_REQUEST


def create_request(client, **changes):
    data = {**VALID_REQUEST, **changes}
    return client.post("/api/requests", json=data)


def test_criar_solicitacao(login_as):
    ana = login_as("ana")
    response = create_request(ana)

    assert response.status_code == 201
    body = response.get_json()["request"]
    assert body["status"] == "ABERTO"
    assert body["requester"] == "Ana"
    assert body["category"] == "TI"


def test_criar_solicitacao_invalida(login_as):
    ana = login_as("ana")

    assert create_request(ana, title="ab").status_code == 400
    assert create_request(ana, description="curta").status_code == 400
    assert create_request(ana, category_id=None).status_code == 400
    assert create_request(ana, category_id=999).status_code == 400


def test_editar_solicitacao_aberta(login_as):
    ana = login_as("ana")
    request_id = create_request(ana).get_json()["request"]["id"]

    response = ana.put(f"/api/requests/{request_id}", json={**VALID_REQUEST, "title": "Novo título"})

    assert response.status_code == 200
    assert response.get_json()["request"]["title"] == "Novo título"


def test_somente_dono_edita_e_exclui(login_as):
    ana = login_as("ana")
    beto = login_as("beto")
    request_id = create_request(ana).get_json()["request"]["id"]

    assert beto.put(f"/api/requests/{request_id}", json=VALID_REQUEST).status_code == 403
    assert beto.delete(f"/api/requests/{request_id}").status_code == 403


def test_nao_edita_nem_exclui_fora_de_aberto(login_as):
    ana = login_as("ana")
    carla = login_as("carla")
    request_id = create_request(ana).get_json()["request"]["id"]
    carla.patch(f"/api/requests/{request_id}/status", json={"status": "EM_ATENDIMENTO"})

    assert ana.put(f"/api/requests/{request_id}", json=VALID_REQUEST).status_code == 409
    assert ana.delete(f"/api/requests/{request_id}").status_code == 409


def test_excluir_solicitacao(login_as):
    ana = login_as("ana")
    request_id = create_request(ana).get_json()["request"]["id"]

    assert ana.delete(f"/api/requests/{request_id}").status_code == 200
    assert ana.get(f"/api/requests/{request_id}").status_code == 404


def test_fluxo_de_status(login_as):
    ana = login_as("ana")
    carla = login_as("carla")
    request_id = create_request(ana).get_json()["request"]["id"]
    url = f"/api/requests/{request_id}/status"

    # solicitante não pode alterar status
    assert ana.patch(url, json={"status": "EM_ATENDIMENTO"}).status_code == 403
    # não pode pular de ABERTO direto para CONCLUIDO
    assert carla.patch(url, json={"status": "CONCLUIDO"}).status_code == 409
    assert carla.patch(url, json={"status": "EM_ATENDIMENTO"}).status_code == 200
    assert carla.patch(url, json={"status": "CONCLUIDO"}).status_code == 200
    # status inexistente
    assert carla.patch(url, json={"status": "XPTO"}).status_code == 400


def test_filtros(login_as):
    ana = login_as("ana")
    carla = login_as("carla")
    create_request(ana, title="Mouse quebrado", category_id=1)
    create_request(ana, title="Férias de julho", category_id=2)
    request_id = create_request(ana, title="Compra de cadeira", category_id=3).get_json()["request"]["id"]
    carla.patch(f"/api/requests/{request_id}/status", json={"status": "EM_ATENDIMENTO"})

    def count(query):
        return len(ana.get(f"/api/requests?{query}").get_json()["items"])

    assert count("") == 3
    assert count("q=mouse") == 1
    assert count("category_id=2") == 1
    assert count("status=EM_ATENDIMENTO") == 1
    assert count("date_from=2000-01-01&date_to=2999-12-31") == 3
    assert count("date_from=2999-01-01") == 0
    assert ana.get("/api/requests?date_from=ontem").status_code == 400


def test_dashboard(login_as):
    ana = login_as("ana")
    carla = login_as("carla")
    request_id = create_request(ana).get_json()["request"]["id"]
    create_request(ana)
    carla.patch(f"/api/requests/{request_id}/status", json={"status": "EM_ATENDIMENTO"})

    assert ana.get("/api/dashboard").get_json() == {
        "total": 2,
        "aberto": 1,
        "em_atendimento": 1,
        "concluido": 0,
    }


def test_listar_categorias(login_as):
    ana = login_as("ana")
    names = [c["name"] for c in ana.get("/api/categories").get_json()["items"]]

    assert names == ["Compras", "RH", "TI"]
