from http import HTTPStatus

from fastapi import FastAPI

from schemas import Message

app = FastAPI()


@app.get("/", status_code=HTTPStatus.OK, response_model=Message)
def read_root():
    return {"message": "Olá, mundo!"}


@app.get("/hello")
def desafio_html():
    return """
        <h1>Olá, mundo!</h1>
    """
