from fastapi import FastAPI
import uvicorn
from routes import auth_router, predict_router

app = FastAPI()

@app.get("/")
async def hello() -> dict:
    return {
        "message": "Hello World!"
    }

@app.get("/health")
async def health() -> dict:
    return {
        "message": "Servidor está no AR!"
    }

app.include_router(auth_router, prefix = "/auth")
app.include_router(predict_router, prefix = "/predict")

if __name__ == "__main__":
    print("Iniciando o Projeto Eventos-API...")
    uvicorn.run("main:app", host="localhost", port=8080, reload=True)