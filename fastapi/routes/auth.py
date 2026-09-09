from fastapi import APIRouter, HTTPException, Depends
from database import auth_user
import security as sc
from fastapi.security import OAuth2PasswordRequestForm

auth_router = APIRouter(
    tags=['Auth']
)

@auth_router.post('/token')
def token(form_data: OAuth2PasswordRequestForm = Depends(OAuth2PasswordRequestForm)) -> dict:
    user = auth_user(login = form_data.username, password=form_data.password)
    if user is None:
        raise HTTPException(status_code=401, detail="Usuário ou senha inválidos")

    return sc.create_token_return(user)