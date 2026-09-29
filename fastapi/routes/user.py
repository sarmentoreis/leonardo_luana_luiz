from fastapi import APIRouter, HTTPException, Depends, status
import database.users as u
import database.connection as c
from sqlmodel import Session
import security as sc
from models import UserResponseDTO, TokenData
import consts.permissions as perm
from typing import List

user_router = APIRouter(
    tags=['User']
)

@user_router.get('/', response_model = List[UserResponseDTO])
async def get_users(token: TokenData = Depends(sc.validate_token), session: Session = Depends(c.get_session)) ->  List[UserResponseDTO]:
    if not token.has_permission(perm.USER_READ): 
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Can't access user's data.") 
    
    user = u.get_all(session=session)
    return user

@user_router.get('/{id}', response_model = UserResponseDTO)
async def get_user_by_id(id: int, token: TokenData = Depends(sc.validate_token), session: Session = Depends(c.get_session)) ->  UserResponseDTO:
    if not token.has_permission(perm.USER_READ): 
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Can't access user's data.") 
    
    user = u.get_user_by_id(id=id, session=session)

    if user is None:
        raise HTTPException( status_code= status.HTTP_404_NOT_FOUND, detail="User não encontrado")

    return user