from fastapi import APIRouter, HTTPException, Depends
import datas as dt
import security as sc
from fastapi.security import OAuth2PasswordRequestForm

auth_router = APIRouter(
    tags=['Auth']
)

@auth_router.post('/token')
def token(form_data: OAuth2PasswordRequestForm = Depends(OAuth2PasswordRequestForm)) -> dict:
    user = dt.get_user_by_login_and_password(login = form_data.username, password=form_data.password)
    if user is None:
        raise HTTPException(status_code=401, detail="Usuário ou senha inválidos")

    return sc.create_token_return(user)