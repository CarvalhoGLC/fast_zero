from http import HTTPStatus

from fastapi.testclient import TestClient


def test_root_deve_retornar_ola_mundo(client: TestClient):

    response = client.get("/")

    assert response.json() == {"message": "Olá, mundo!"}
    assert response.status_code == HTTPStatus.OK


def test_create_user(client: TestClient):

    response = client.post(
        "/users",
        json={
            "username": "alice",
            "email": "alice@example.com",
            "password": "secret",
        },
    )

    assert response.status_code == HTTPStatus.CREATED
    assert response.json() == {
        "username": "alice",
        "email": "alice@example.com",
        "id": 1,
    }


def test_read_users(client: TestClient):

    response = client.get("/users")

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {
        "users": [
            {
                "username": "alice",
                "email": "alice@example.com",
                "id": 1,
            }
        ]
    }


def test_update_user(client: TestClient):

    response = client.put(
        "/users/1",
        json={
            "username": "bob",
            "email": "bob@example.com",
            "password": "secret",
        },
    )

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {
        "username": "bob",
        "email": "bob@example.com",
        "id": 1,
    }


def test_update_user_not_found(client):
    response = client.put(
        "/users/-1",
        json={
            "username": "Jessica",
            "email": "jessica@example.com",
            "password": "secret123",
        },
    )

    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json() == {"detail": "User not found!"}


def test_get_id_user(client):
    response = client.get("/users/1")

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {
        "username": "bob",
        "email": "bob@example.com",
        "id": 1,
    }


def test_get_id_user_not_found(client):
    response = client.get("/users/-1")

    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json() == {"detail": "ID not found!"}


def test_delete_user(client: TestClient):
    response = client.delete("users/1")

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {
        "username": "bob",
        "email": "bob@example.com",
        "id": 1,
    }


def test_delete_user_not_found(client):
    response = client.delete("users/-1")

    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json() == {"detail": "User not found!"}
