from fastapi import APIRouter, HTTPException, Depends, status
import database.users as u
import database.connection as c
from sqlmodel import Session
import security as sc
from models.user import UserResponseDTO

user_router = APIRouter(
    tags=['User']
)

@user_router.get('/{id}', response_model = UserResponseDTO)
async def get_user_by_id(id: int, token: str = Depends(sc.validate_token), session: Session = Depends(c.get_session)) ->  UserResponseDTO:
    user = u.get_user_by_id(id=id, session=session)

    if user is None:
        raise HTTPException( status_code= status.HTTP_404_NOT_FOUND, detail="User não encontrado")

    if user.login != token:
        raise HTTPException( status_code= status.HTTP_403_FORBIDDEN, detail="Acesso restrito")

    return user