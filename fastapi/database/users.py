import security as sec
from fastapi import  Depends
from models import User, UserRequestDTO
from sqlmodel import Session, select
from database import get_session

def auth_user(login: str, password: str, session: Session = Depends(get_session)) -> User | None:
    statement = select(User).where(
        User.login == login
    )
    user = session.exec(statement).first()

    if not sec.verify_password(password, user.hash_password):
        return None
    
    return user 

def get_user_by_login(login: str, session: Session = Depends(get_session)) -> User | None:
    statement = select(User).where(
        User.login == login
    )

    return session.exec(statement).first()

def get_user_by_id(id: int, session: Session = Depends(get_session)) -> User | None:
    statement = select(User).where(
        User.id == id
    )
    
    return session.exec(statement).first()

def create_user(dto: UserRequestDTO, session: Session = Depends(get_session)) -> User:
    user = User(login=dto.login, name=dto.name, email=dto.email, hash_password=sec.hash_password(dto.password))

    session.add(user)
    session.commit()
    session.refresh(user)

    return user

def edit_user( id: int, dto: UserRequestDTO, session: Session = Depends(get_session)) -> User | None:
    user = get_user_by_id(id, session)

    if user is None:
        return None

    user.login = dto.login
    user.name = dto.name
    user.email = dto.email
    user.hash_password = sec.hash_password(dto.password)

    session.commit()
    session.refresh(user)

    return user

def delete_user(id: int, session: Session = Depends(get_session)) -> bool:
    user = get_user_by_id(id, session)

    if user is None:
        return False

    session.delete(user)
    session.commit()

    return True