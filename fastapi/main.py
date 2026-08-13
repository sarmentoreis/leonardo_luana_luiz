from fastapi import FastAPI
import uvicorn
from routes.user import user_router

app = FastAPI()

@app.get("/")
async def home() -> dict:
    return {
        "message": "O Servidor está no AR!"
    }

@app.get("/health")
async def health() -> dict:
    return {
        "message": "Servidor OK!"
    }

app.include_router(user_router, prefix = "/user")

if __name__ == "__main__":
    print("Iniciando o Projeto Eventos-API...")
    uvicorn.run("main:app", host="localhost", port=8080, reload=True)