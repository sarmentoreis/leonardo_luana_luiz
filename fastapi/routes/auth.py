from fastapi import APIRouter, HTTPException, Request, Depends, status
import database.users as u
import database.connection as c
from sqlmodel import Session
import security as sc
from fastapi.security import OAuth2PasswordRequestForm
from models.user import UserSignInRequestDTO, UserRequestDTO, UserResponseDTO

auth_router = APIRouter(
    tags=['Auth']
)
@auth_router.post('/signup', status_code  = status.HTTP_201_CREATED,  response_model=UserResponseDTO)
@sc.limiter.limit("5/minute")
async def signup(request: Request, body: UserRequestDTO, session: Session = Depends(c.get_session)) -> UserResponseDTO:
    user = u.create_user(dto=body, session=session)    
    if user is None:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="User already exists")
    
    return user 

@auth_router.post('/signin')
@sc.limiter.limit("5/minute")
async def signin(request: Request,dto: UserSignInRequestDTO, session: Session = Depends(c.get_session)) -> dict:
    user = u.auth_user(login = dto.login, password=dto.password, session=session)
    if user is None:
        raise HTTPException(status_code=401, detail="Usuário ou senha inválidos")

    return sc.create_token_return(user)

@auth_router.post('/token')
@sc.limiter.limit("5/minute")
def token(request: Request, form_data: OAuth2PasswordRequestForm = Depends(OAuth2PasswordRequestForm), session: Session = Depends(c.get_session)) -> dict:
    user = u.auth_user(login = form_data.username, password=form_data.password, session=session)
    if user is None:
        raise HTTPException(status_code=401, detail="Usuário ou senha inválidos")

    return sc.create_token_return(user)