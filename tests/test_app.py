from http import HTTPStatus

from fastapi.testclient import TestClient

from schemas import UserPublic


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


def test_create_user_integrity_error(client, user):
    client.post(
        "/users",
        json={
            "username": "alice",
            "email": "alice@example.com",
            "password": "secret",
        },
    )

    response = client.post(
        "/users",
        json={
            "username": "alice",
            "email": "alice1@example.com",
            "password": "secret",
        },
    )

    assert response.status_code == HTTPStatus.CONFLICT
    assert response.json() == {"detail": "Username already exists"}


def test_create_email_integrity_error(client, user):
    client.post(
        "/users",
        json={
            "username": "alice",
            "email": "alice@example.com",
            "password": "secret",
        },
    )

    response = client.post(
        "/users",
        json={
            "username": "marcus",
            "email": "alice@example.com",
            "password": "secret",
        },
    )

    assert response.status_code == HTTPStatus.CONFLICT
    assert response.json() == {"detail": "Email already exists"}


def test_read_users(client: TestClient):

    response = client.get("/users")

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {"users": []}


def test_read_with_users(client: TestClient, user):

    user_schema = UserPublic.model_validate(user).model_dump()

    response = client.get("/users")

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {"users": [user_schema]}


def test_update_user(client: TestClient, user):

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


def test_update_integrity_error(client, user):
    client.post(
        "/users",
        json={
            "username": "fausto",
            "email": "fausto@example.com",
            "password": "secret",
        },
    )

    response = client.put(
        f"/users/{user.id}",
        json={
            "username": "fausto",
            "email": "bob@example.com",
            "password": "mynewpassword",
        },
    )

    assert response.status_code == HTTPStatus.CONFLICT
    assert response.json() == {"detail": "Username or Email already exists"}


def test_get_id_user(client, user):
    user_schema = UserPublic.model_validate(user).model_dump()

    response = client.get(f"/users/{user.id}")

    assert response.status_code == HTTPStatus.OK
    assert response.json() == user_schema


def test_get_id_user_not_found(client, user):

    response = client.get("/users/-1")

    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json() == {"detail": "ID not found!"}


def test_delete_user(client: TestClient, user):
    response = client.delete("/users/1")

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {"message": "User deleted!"}


def test_delete_user_not_found(client, user):
    response = client.delete("users/-1")

    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json() == {"detail": "User not found!"}
