from fastapi import APIRouter
from models.base import Usuario

router = APIRouter()


@router.post("/usuarios")
def criar_usuario(usuario: Usuario):
    return {
        "message": "Usuário criado com sucesso",
        "usuario": usuario
    }