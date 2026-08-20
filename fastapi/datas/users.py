from models import User
from typing import Dict
import uuid

Users: Dict[str, User] = {
    'usuario.1': User(
        id = 1,
        login = "usuario.1",
        name = 'Admin',
        email = 'admin@email.com.br',
        password = '123',
        audit_token = str(uuid.uuid4())
    )
}

def get_user_by_login_and_password(login: str, password: str) -> User:
    global Users

    if login not in Users:
        return None

    user = Users[login]

    if user.password != password:
        return None
    
    return user


def get_user_by_login(login: str) -> User:
    global Users

    if login not in Users:
        return None

    user = Users[login]
    
    return user