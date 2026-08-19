from fastapi import APIRouter, HTTPException, status, Request, Depends
from models.user import User, UserRequestDTO, UserResponseDTO, UserSignInRequestDTO
from typing import List, Dict
import uuid

user_router = APIRouter(
    tags=['Users']
)

users: Dict[str, User] = {
    'user.teste.1@email.com.br': User(
        id = 1,
        name = 'User Teste 1',
        email = 'user.teste.1@email.com.br',
        password = '456',
        audit_token = str(uuid.uuid4())
    ),
    'user.teste.2@email.com.br': User(
        id = 2,
        name = 'User Teste 2',
        email = 'user.teste.2@email.com.br',
        password = '123',
        audit_token = str(uuid.uuid4())
    ),
    'user.teste.3@email.com.br': User(
        id = 3,
        name = 'User Teste 3',
        email = 'user.teste.3@email.com.br',
        password = 'senha',
        audit_token = str(uuid.uuid4())
    ),
}

users_ids = 4

@user_router.post('/signup', status_code  = status.HTTP_201_CREATED,  response_model=UserResponseDTO)
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


@user_router.post('/signin')
async def signin(body: UserSignInRequestDTO) -> dict:
    if body.email not in users:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid credentials!")

    user = users[body.email]

    if user.password != body.password:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid credentials!")

    return {
        "message": "User signed in successfully"
    }


