from dataclasses import asdict
from datetime import datetime

from sqlalchemy import select

from fast_zero.models import User


def test_create_user(session, mock_db_time):

    with mock_db_time(model=User) as time:
        new_user = User(
            username="Guilherme",
            email="gui@example.com",
            password="123456",
            updated_at=datetime.now(),
        )
        session.add(new_user)
        session.commit()

        user = session.scalar(select(User).where(User.username == "Guilherme"))

    assert asdict(user) == {
        "id": 1,
        "username": "Guilherme",
        "email": "gui@example.com",
        "password": "123456",
        "created_at": time,
        "updated_at": time,
    }
