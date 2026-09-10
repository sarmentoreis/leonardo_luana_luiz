from fastapi import APIRouter, Depends, HTTPException, status
import security as sc
import database.users as u
import database.predict as p
from typing import List
from models import Predict, PredictRequestDTO, PredictResponseDTO

predict_router = APIRouter(
    tags=['Predict']
)

@predict_router.post('/', response_model=PredictResponseDTO)
async def post_predict(body: PredictRequestDTO, token: str = Depends(sc.validate_token)) -> PredictResponseDTO:
    user = u.get_user_by_login(token)
    
    if user is None:
        raise HTTPException( status_code= status.HTTP_403_FORBIDDEN, detail="Acesso restrito")
    
    prediction = p.create_predict(body, user.id)

    return prediction

@predict_router.get('/my-predictions', response_model = List[PredictResponseDTO])
async def get_predictions(token: str = Depends(sc.validate_token)) ->  List[PredictResponseDTO]:
    user = p.get_user_by_login(token)

    if user is None:
        raise HTTPException( status_code= status.HTTP_403_FORBIDDEN, detail="Acesso restrito")

    predictions = p.get_all_predicts_by_owner_id(user.id)

    return predictions

@predict_router.get('/my-predictions/{id}', response_model = PredictResponseDTO)
async def get_predict_by_id(id: int, token: str = Depends(sc.validate_token)) ->  PredictResponseDTO:
    user = u.get_user_by_login(token)

    if user is None:
        raise HTTPException( status_code= status.HTTP_403_FORBIDDEN, detail="Acesso restrito")

    prediction = p.get_predict_by_id(id)

    if prediction is None:
        raise HTTPException( status_code= status.HTTP_404_NOT_FOUND, detail="Prediction não existe")

    if prediction.owner_id != user.id:
        raise HTTPException( status_code= status.HTTP_403_FORBIDDEN, detail="Acesso restrito")

    return prediction

@predict_router.delete('/my-predictions/{id}', response_model = dict)
async def delete_predict(id: int, token: str = Depends(sc.validate_token)) -> dict:
    user = u.get_user_by_login(token)

    if user is None:
        raise HTTPException( status_code= status.HTTP_403_FORBIDDEN, detail="Acesso restrito")

    prediction = p.get_predict_by_id(id)

    if prediction is None:
        raise HTTPException( status_code= status.HTTP_404_NOT_FOUND, detail="Prediction não existe")

    if prediction.owner_id != user.id:
        raise HTTPException( status_code= status.HTTP_403_FORBIDDEN, detail="Acesso restrito")

    prediction = p.delete_predict(id)

    return {"message": "Predict deletado com sucesso."}