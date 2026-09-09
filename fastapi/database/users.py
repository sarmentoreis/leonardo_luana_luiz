from fastapi import  Depends
from models import User
from sqlmodel import Session, select
from database import get_session
from security.hash import verify_password

def auth_user(login: str, password: str, session: Session = Depends(get_session)) -> User | None:
    statement = select(User).where(
        User.login == login
    )
    user = session.exec(statement).first()

    if not verify_password(password, user.hash_password):
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