from fastapi import APIRouter
from models.user import User

user_router = APIRouter(tags=['Users'])


@user_router.post("/usuarios")
def criar_usuario(usuario: User):
    return {
        "message": "Usuário criado com sucesso",
        "usuario": usuario
    }