from fastapi import FastAPI, Request
from fastapi.responses import RedirectResponse
from fastapi.middleware.cors import CORSMiddleware
from sqlmodel import SQLModel
import uvicorn
from routes import auth_router, predict_router, user_router
from database import engine
from slowapi.errors import RateLimitExceeded
from slowapi import _rate_limit_exceeded_handler
import time
from security import limiter
from models import *

origins = [
    "http://localhost",
    "http://localhost:8080",
    "https://localhost",
    "https://localhost:8080",
    "https://example.com",
    "https://www.example.com",
    "http://localhost:3000",
]


app = FastAPI()
SQLModel.metadata.create_all(engine)

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["GET, PUT, POST, DELETE"],
    allow_headers=["*"],
)

app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

@app.get("/")
async def hello() -> dict:
    return RedirectResponse(url="/docs")

@app.get("/health")
async def health() -> dict:
    return {
        "message": "Servidor está no AR!"
    }

@app.middleware("http")
async def add_headers(request: Request, call_next):
    start_time = time.perf_counter()
    response = await call_next(request)
    process_time = time.perf_counter() - start_time
    response.headers["X-Process-Time"] = str(process_time)
    response.headers["X-Frame-Options"] = "DENY"
    response.headers["X-Content-Type-Options"] = "nosniff"
    response.headers["Strict-Transport-Security"] = "max-age=31536000; includeSubDomains"
    response.headers["Content-Security-Policy"] = (
        "default-src 'self'; "
        "script-src 'self' https://cdn.jsdelivr.net 'unsafe-inline'; "
        "style-src 'self' https://cdn.jsdelivr.net 'unsafe-inline'; "
        "img-src 'self' data: https://fastapi.tiangolo.com; "
        "font-src 'self' https://cdn.jsdelivr.net; "
        "connect-src 'self' https://cdn.jsdelivr.net;"
    ) # Maldito Swagger

    return response

app.include_router(auth_router, prefix = "/auth")
app.include_router(user_router, prefix = "/user")
app.include_router(predict_router, prefix = "/predict")

if __name__ == "__main__":
    print("Iniciando o Projeto de Bloco...")
    uvicorn.run("main:app", host="localhost", port=8080, reload=True)