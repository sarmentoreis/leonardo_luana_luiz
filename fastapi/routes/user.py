from fastapi import APIRouter, Depends, HTTPException, status
import security as sc
import database.users as u
from models import UserRequestDTO, UserResponseDTO

predict_router = APIRouter(
    tags=['User']
)

@predict_router.post('/', response_model=UserResponseDTO)
async def post_user(body: UserRequestDTO, token: str = Depends(sc.validate_token)) -> UserResponseDTO:
    user = u.get_user_by_login(token)
    
    if user is None:
        raise HTTPException( status_code= status.HTTP_403_FORBIDDEN, detail="Acesso restrito")
    
    newUser = u.create_user(body)

    return newUser