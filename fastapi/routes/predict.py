from fastapi import APIRouter, Depends, HTTPException, status
import security as sc
import database.users as u
import database.predict as p
import database.connection as c
from sqlmodel import Session
from typing import List
from models import PredictRequestDTO, PredictResponseDTO

predict_router = APIRouter(
    tags=['Predict']
)

@predict_router.post('/', status_code  = status.HTTP_201_CREATED, response_model=PredictResponseDTO)
async def post_predict(body: PredictRequestDTO, token: str = Depends(sc.validate_token), session: Session = Depends(c.get_session)) -> PredictResponseDTO:
    user = u.get_user_by_login(login=token, session=session)
    
    if user is None:
        raise HTTPException( status_code= status.HTTP_403_FORBIDDEN, detail="Acesso restrito")
    
    prediction = p.create_predict(dto=body, owner_id=user.id, session=session)

    return prediction

@predict_router.get('/', response_model = List[PredictResponseDTO])
async def get_predictions(token: str = Depends(sc.validate_token), session: Session = Depends(c.get_session)) ->  List[PredictResponseDTO]:
    user = u.get_user_by_login(login=token, session=session)

    if user is None:
        raise HTTPException( status_code= status.HTTP_403_FORBIDDEN, detail="Acesso restrito")

    predictions = p.get_all_predicts_by_owner_id(owner_id=user.id, session=session)

    return predictions

@predict_router.get('/{id}', response_model = PredictResponseDTO)
async def get_predict_by_id(id: int, token: str = Depends(sc.validate_token), session: Session = Depends(c.get_session)) ->  PredictResponseDTO:
    user = u.get_user_by_login(login=token, session=session)

    if user is None:
        raise HTTPException(status_code= status.HTTP_403_FORBIDDEN, detail="Acesso restrito")

    prediction = p.get_predict_by_id(id=id, session=session)

    if prediction is None:
        raise HTTPException(status_code= status.HTTP_404_NOT_FOUND, detail="Prediction não existe")

    if prediction.owner_id != user.id:
        raise HTTPException(status_code= status.HTTP_403_FORBIDDEN, detail="Acesso restrito")

    return prediction

@predict_router.delete('/{id}', response_model = dict)
async def delete_predict(id: int, token: str = Depends(sc.validate_token), session: Session = Depends(c.get_session)) -> dict:
    user = u.get_user_by_login(login=token, session=session)

    if user is None:
        raise HTTPException(status_code= status.HTTP_403_FORBIDDEN, detail="Acesso restrito")

    prediction = p.get_predict_by_id(id=id, session=session)

    if prediction is None:
        raise HTTPException(status_code= status.HTTP_404_NOT_FOUND, detail="Predict não existe")

    if prediction.owner_id != user.id:
        raise HTTPException(status_code= status.HTTP_403_FORBIDDEN, detail="Acesso restrito")

    prediction = p.delete_predict(id=id, session=session)

    return {"message": "Predict deletado com sucesso."}