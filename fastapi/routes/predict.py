from fastapi import APIRouter

predict_router = APIRouter(
    tags=['Predict']
)

@predict_router.post('/')
async def post_predict(body: str) -> dict:

    return {
        "message": "Batata"
    }