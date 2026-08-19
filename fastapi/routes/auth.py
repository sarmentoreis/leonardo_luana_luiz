from fastapi import APIRouter, HTTPException, status
from models import User, UserRequestDTO, UserResponseDTO, UserSignInRequestDTO
from typing import Dict
import uuid

auth_router = APIRouter(
    tags=['Auth']
)

users: Dict[str, User] = {
    'admin@email.com.br': User(
        id = 1,
        name = 'Admin',
        email = 'admin@email.com.br',
        password = '123',
        audit_token = str(uuid.uuid4())
    )
}

users_ids = 2

@auth_router.post('/signup', status_code  = status.HTTP_201_CREATED,  response_model=UserResponseDTO)
async def signup(body: UserRequestDTO) -> UserResponseDTO:
    global users_ids

    if body.email in users:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="User already exists")

    user = User(
        id = users_ids,
        name = body.name,
        email = body.email,
        password = body.password,
        audit_token = str(uuid.uuid4())
    )

    users_ids += 1
    users.append(user)
    
    return user 


@auth_router.post('/token')
async def signin(body: UserSignInRequestDTO) -> dict:
    if body.email not in users:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid credentials!")

    user = users[body.email]

    if user.password != body.password:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid credentials!")

    return {
        "message": "User signed in successfully"
    }


