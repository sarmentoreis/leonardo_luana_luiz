from fastapi import APIRouter, HTTPException, Depends, status
import database.users as u
import security as sc
from fastapi.security import OAuth2PasswordRequestForm
from models.user import UserSignInRequestDTO, UserRequestDTO, UserResponseDTO

auth_router = APIRouter(
    tags=['Auth']
)
@auth_router.post('/signup', status_code  = status.HTTP_201_CREATED,  response_model=UserResponseDTO)
async def signup(body: UserRequestDTO) -> UserResponseDTO:
    user = u.create_user(body)    
    if user is None:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="User already exists")
    
    return user 

@auth_router.post('/signin')
async def signin(dto: UserSignInRequestDTO) -> dict:
    user = u.auth_user(login = dto.login, password=dto.password)
    if user is None:
        raise HTTPException(status_code=401, detail="Usuário ou senha inválidos")

    return sc.create_token_return(user)

@auth_router.post('/token')
def token(form_data: OAuth2PasswordRequestForm = Depends(OAuth2PasswordRequestForm)) -> dict:
    user = u.auth_user(login = form_data.username, password=form_data.password)
    if user is None:
        raise HTTPException(status_code=401, detail="Usuário ou senha inválidos")

    return sc.create_token_return(user)