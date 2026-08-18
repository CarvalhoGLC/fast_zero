from http import HTTPStatus

from fastapi.testclient import TestClient

from fast_zero.app import app


def test_root_deve_retornar_ola_mundo():
    client = TestClient(app)

    response = client.get("/")

    assert response.json() == {"message": "Olá, mundo!"}
    assert response.status_code == HTTPStatus.OK


def test_desafio_deve_retornar_ola_mundo():
    new_client = TestClient(app)
    
    response = new_client.get("/hello")
    
    assert response.json() == "<h1>Olá, mundo!</h1>"