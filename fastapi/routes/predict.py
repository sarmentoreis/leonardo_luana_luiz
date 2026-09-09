from fastapi import APIRouter, Depends, HTTPException, status
import security as sc
from database import get_user_by_login, get_all_predicts_by_owner_id
from typing import List
from models import Predict

predict_router = APIRouter(
    tags=['Predict']
)

@predict_router.post('/')
async def post_predict(body: str, token: str = Depends(sc.validate_token)) -> dict:

    return {
        "message": "Teste123456"
    }

@predict_router.get('/MyPredictions', response_model = List[Predict])
async def post_predict(token: str = Depends(sc.validate_token)) ->  List[Predict]:
    user = get_user_by_login(token)

    if user is None:
        raise HTTPException( status_code= status.HTTP_403_FORBIDDEN, detail="Acesso restrito")

    predictions = get_all_predicts_by_owner_id(user.id)

    return predictions