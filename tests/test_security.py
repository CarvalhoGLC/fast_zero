from http import HTTPStatus

from jwt import decode

from fast_zero.security import create_access_token
from fast_zero.settings import settings


def test_jwt():
    data = {"test": "test"}
    token = create_access_token(data)

    decoded = decode(token, settings.SECRET_KEY, algorithms=settings.ALGORITHM)

    assert decoded["test"] == data["test"]
    assert "exp" in decoded


def test_jwt_invalid(client, user):
    response = client.delete(
        f"/users/{user.id}", headers={"Authorization": "Bearer token-invalido"}
    )

    assert response.status_code == HTTPStatus.UNAUTHORIZED
    assert response.json() == {"detail": "Could not validate credentials"}


def test_token_invalid_user(client):
    token = create_access_token(data={"sub": "alala@example.com"})

    response = client.get(
        "/users", headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == HTTPStatus.UNAUTHORIZED
    assert response.json() == {"detail": "Could not validate credentials"}


def test_token_invalid_sub(client):
    token = create_access_token(data={"foo": "bar"})

    response = client.get(
        "/users", headers={"Authorization": f"Bearer {token}"}
    )

    assert response.status_code == HTTPStatus.UNAUTHORIZED
    assert response.json() == {"detail": "Could not validate credentials"}
