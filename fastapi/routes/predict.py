from fastapi import APIRouter, Depends
import security as sc

predict_router = APIRouter(
    tags=['Predict']
)
@predict_router.get('/hello')
async def get_predict(token: str = Depends(sc.validate_token)) -> dict:
    
    return {
        "message": "Hello World GPT 50.0"
    }

@predict_router.post('/')
async def post_predict(body: str, token: str = Depends(sc.validate_token)) -> dict:

    return {
        "message": "Teste123456"
    }