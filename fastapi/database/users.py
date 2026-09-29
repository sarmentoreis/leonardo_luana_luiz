import security as sec
from models import User, UserRequestDTO
from sqlmodel import Session, select
from consts.roles import USER_ROLE
from typing import List

def auth_user(login: str, password: str, session: Session) -> User | None:
    statement = select(User).where(
        User.login == login
    )
    user = session.exec(statement).first()

    if user is None:
        return None

    if not sec.verify_password(password, user.hash_password):
        return None
    
    return user 

def get_all(session: Session) -> List[User]:  
    statement = select(User)
    
    return session.exec(statement).fetchall()

def get_user_by_login(login: str, session: Session) -> User | None:
    statement = select(User).where(
        User.login == login
    )

    return session.exec(statement).first()

def get_user_by_id(id: int, session: Session) -> User | None:
    statement = select(User).where(
        User.id == id
    )
    
    return session.exec(statement).first()

def create_user(dto: UserRequestDTO, session: Session) -> User:
    existing_user = get_user_by_login(dto.login)
    if existing_user is not None:
        return None

    user = User(login=dto.login, name=dto.name, email=dto.email, hash_password=sec.hash_password(dto.password), role= USER_ROLE)

    session.add(user)
    session.commit()
    session.refresh(user)

    return user

def edit_user( id: int, dto: UserRequestDTO, session: Session) -> User | None:
    user = get_user_by_id(id, session)

    if user is None:
        return None

    if user.login != dto.login:
        existing_user = get_user_by_login(dto.login)
        if existing_user is not None:
            return None

    user.login = dto.login
    user.name = dto.name
    user.email = dto.email
    user.hash_password = sec.hash_password(dto.password)

    session.commit()
    session.refresh(user)

    return user

def delete_user(id: int, session: Session) -> bool:
    user = get_user_by_id(id, session)

    if user is None:
        return False

    session.delete(user)
    session.commit()

    return True