from datetime import datetime
from http import HTTPStatus

from fastapi import Depends, FastAPI, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from fast_zero.database import get_session
from fast_zero.models import User
from fast_zero.security import get_password_hash, verify_password
from schemas import Message, Token, UserList, UserPublic, UserSchema

app = FastAPI()


@app.post("/users", status_code=HTTPStatus.CREATED, response_model=UserPublic)
def create_user(user: UserSchema, session=Depends(get_session)):
    db_user = session.scalar(
        select(User).where(
            (User.username == user.username) | (User.email == user.email)
        )
    )

    if db_user:
        if db_user.username == user.username:
            raise HTTPException(
                detail="Username already exists",
                status_code=HTTPStatus.CONFLICT,
            )
        elif db_user.email == user.email:
            raise HTTPException(
                detail="Email already exists", status_code=HTTPStatus.CONFLICT
            )

    db_user = User(
        username=user.username,
        email=user.email,
        password=get_password_hash(user.password),
        updated_at=datetime.now(),
    )

    session.add(db_user)
    session.commit()
    session.refresh(db_user)

    return db_user


@app.get("/users", status_code=HTTPStatus.OK, response_model=UserList)
def read_users(limit=10, offset=0, session=Depends(get_session)):
    users = session.scalars(select(User).limit(limit).offset(offset))
    return {"users": users}


@app.put(
    "/users/{user_id}", status_code=HTTPStatus.OK, response_model=UserPublic
)
def update_user(user_id: int, user: UserSchema, session=Depends(get_session)):
    user_db = session.scalar(select(User).where(User.id == user_id))

    if not user_db:
        raise HTTPException(
            detail="User not found!", status_code=HTTPStatus.NOT_FOUND
        )

    try:
        user_db.username = user.username
        user_db.email = user.email
        user_db.password = get_password_hash(user.password)

        session.commit()
        session.refresh(user_db)

        return user_db
    except IntegrityError:
        raise HTTPException(
            detail="Username or Email already exists",
            status_code=HTTPStatus.CONFLICT,
        )


@app.delete(
    "/users/{user_id}", status_code=HTTPStatus.OK, response_model=Message
)
def delete_user(user_id: int, session=Depends(get_session)):
    user_db = session.scalar(select(User).where(User.id == user_id))

    if not user_db:
        raise HTTPException(
            detail="User not found!", status_code=HTTPStatus.NOT_FOUND
        )

    session.delete(user_db)
    session.commit()

    return Message(message="User deleted!")


@app.get("/users/{id}", status_code=HTTPStatus.OK, response_model=UserPublic)
def get_id_user(id: int, session=Depends(get_session)):
    user_db = session.scalar(select(User).where(User.id == id))
    if not user_db:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND, detail="ID not found!"
        )

    return user_db

@app.post("/token", response_model=Token)
def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends(), session: Session = Depends(get_session)):
    user = session.scalar(select(User).where(User.email == form_data.username))
    
    if not user:
        raise HTTPException(
            status_code=HTTPStatus.UNAUTHORIZED,
            detail="Incorrect email or password"
        )
        
    if not verify_password(form_data.password, user.password):
        raise HTTPException(
            status_code=HTTPStatus.UNAUTHORIZED,
            detail="Incorrect email or password"
        )