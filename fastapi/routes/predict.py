from fastapi import APIRouter, Depends, HTTPException, Path, status
import joblib
import security as sc
import database.users as u
import database.predict as p
import database.connection as c
from sqlmodel import Session
from typing import List
from models import PredictRequestDTO,  PredictFullResponseDTO, TokenData
import consts.permissions as perm
from pathlib import Path

predict_router = APIRouter(
    tags=['Predict']
)

@predict_router.post('/', status_code  = status.HTTP_201_CREATED, response_model=PredictFullResponseDTO)
async def post_predict(body: PredictRequestDTO, token: TokenData = Depends(sc.validate_token), session: Session = Depends(c.get_session)) -> PredictFullResponseDTO:
    if not token.has_permission(perm.PREDICT_CREATE): 
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Can't create predict's data.") 
       
    prediction = p.create_predict(dto=body, owner_id=token.entity_id, session=session)
    return prediction

@predict_router.get('/', response_model = List[PredictFullResponseDTO])
async def get_predictions(token: TokenData = Depends(sc.validate_token), session: Session = Depends(c.get_session)) ->  List[PredictFullResponseDTO]:
    if not token.has_permission(perm.PREDICT_READ): 
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Can't access predict's data.") 

    predictions = p.get_all_predicts_by_owner_id(owner_id=token.entity_id, session=session)
    return predictions

@predict_router.get('/{id}', response_model = PredictFullResponseDTO)
async def get_predict_by_id(id: int, token: TokenData = Depends(sc.validate_token), session: Session = Depends(c.get_session)) ->  PredictFullResponseDTO:
    if not token.has_permission(perm.PREDICT_READ): 
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Can't access predict's data.") 

    prediction = p.get_predict_by_id(id=id, session=session)

    if prediction is None:
        raise HTTPException(status_code= status.HTTP_404_NOT_FOUND, detail="Prediction não existe")

    print(prediction.owner_id, token.entity_id)
    if not token.has_owner_id(prediction.owner_id):
        raise HTTPException(status_code= status.HTTP_403_FORBIDDEN, detail="Acesso restrito")

    return prediction

@predict_router.delete('/{id}', response_model = dict)
async def delete_predict(id: int, token: TokenData = Depends(sc.validate_token), session: Session = Depends(c.get_session)) -> dict:
    if not token.has_permission(perm.PREDICT_DELETE): 
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Can't delete predict's data.") 

    prediction = p.get_predict_by_id(id=id, session=session)

    if prediction is None:
        raise HTTPException(status_code= status.HTTP_404_NOT_FOUND, detail="Predict não existe")

    if not token.has_owner_id(prediction.owner_id):
        raise HTTPException(status_code= status.HTTP_403_FORBIDDEN, detail="Acesso restrito")

    prediction = p.delete_predict(id=id, session=session)

    return {"message": "Predict deletado com sucesso."}

@predict_router.post('/classify', status_code  = status.HTTP_200_OK, response_model=PredictFullResponseDTO)
async def post_classify(body: PredictRequestDTO, token: TokenData = Depends(sc.validate_token), session: Session = Depends(c.get_session)) -> PredictFullResponseDTO:
    if not token.has_permission(perm.PREDICT_CREATE): 
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Can't classify data.") 

    texto = body.text.strip()
    if not texto:
            raise HTTPException(
                status_code=422,
                detail="A mensagem não pode estar vazia"
            )
            
    BASE_DIR = Path(__file__).resolve().parent.parent
    JOBLIB_DIR = BASE_DIR / "joblib"
    
    MODEL_PATH = JOBLIB_DIR / "melhor_classificador_intent.joblib"
    modelo = joblib.load(MODEL_PATH)
    VECTOR_PATH = JOBLIB_DIR / "vectorizer.joblib"
    vectorizer = joblib.load(VECTOR_PATH)

    X = vectorizer.transform([texto])
    intent = modelo.predict(X)[0]
    probability = modelo.predict_proba(X).max()

    prediction = p.create_predict(dto=body, owner_id=token.entity_id, session=session, intent=intent, probability=probability)

    return prediction