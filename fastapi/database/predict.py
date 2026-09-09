from fastapi import  Depends
from models import Predict
from sqlmodel import Session, select
from database import get_session
from typing import List

def get_predict_by_id(id: int, session: Session = Depends(get_session)) -> Predict | None:
    statement = select(Predict).where(
        Predict.id == id
    )
    
    return session.exec(statement).first()

def get_all_predicts_by_owner_id(owner_id: int, session: Session = Depends(get_session)) -> List[Predict]:
    statement = select(Predict).where(
        Predict.owner_id == owner_id
    )
    
    return session.exec(statement).fetchall()


def get_all_predicts_by_intent(intent: str, session: Session = Depends(get_session)) -> List[Predict]:
    statement = select(Predict).where(
        Predict.intent == intent
    )
    
    return session.exec(statement).fetchall()