from models import Predict, PredictRequestDTO
from sqlmodel import Session, select
from typing import List

def get_all(session: Session) -> List[Predict]:  
    statement = select(Predict)
    
    return session.exec(statement).fetchall()

def get_predict_by_id(id: int, session: Session) -> Predict | None:
    statement = select(Predict).where(
        Predict.id == id
    )
    
    return session.exec(statement).first()

def get_all_predicts_by_owner_id(owner_id: int, session: Session) -> List[Predict]:   
    statement = select(Predict).where(
        Predict.owner_id == owner_id
    )
    
    return session.exec(statement).fetchall()


def get_all_predicts_by_intent(intent: str, session: Session) -> List[Predict]:
    statement = select(Predict).where(
        Predict.intent == intent
    )
    
    return session.exec(statement).fetchall()

def create_predict(dto: PredictRequestDTO, owner_id: int, session: Session) -> Predict:
    predict = Predict(text=dto.text, intent="Cancelamento", owner_id=owner_id)

    session.add(predict)
    session.commit()
    session.refresh(predict)

    return predict

def delete_predict(id: int, session: Session) -> bool:
    predict = get_predict_by_id(id, session)

    if predict is None:
        return False

    session.delete(predict)
    session.commit()

    return True