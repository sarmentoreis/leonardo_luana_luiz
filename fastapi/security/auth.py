import jwt
from jwt.exceptions import InvalidTokenError
from datetime import datetime, timezone, timedelta
from models import User
from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer

SECRET_KEY = "MinhaChaveSecretaJWT2026_ABC123!"
TOKEN_DURATION_MINUTES = 30
TOKEN_ALGORITHM = "HS256"
TOKEN_URL = "/token"
TOKEN_TYPE = "Bearer"

oauth2_scheme = OAuth2PasswordBearer(tokenUrl=TOKEN_URL)

def create_token(user: User) -> str:
    expiracao = datetime.now(timezone.utc) + timedelta(minutes=30)
    dados = {
        "sub": user.login,
        "exp": expiracao
    }
    token = jwt.encode(payload = dados, key = SECRET_KEY, algorithm = TOKEN_ALGORITHM)
    return token

def create_token_return(user: User):
    token = create_token(user = user)
    return {
        "access_token": token,
        "token_type": TOKEN_TYPE
    }

def validate_token(token: str = Depends(oauth2_scheme)):
    error = HTTPException(
        status_code=401,
        detail="Token inválido ou expirado",
        headers={"WWW-Authenticate": TOKEN_TYPE}
    )

    try:
        result = jwt.decode(payload = token, key = SECRET_KEY, algorithm = [TOKEN_ALGORITHM])

        if result is None:
            raise error

        login = result.get('sub')

        if login is None:
            raise error
        
    except InvalidTokenError:
        raise error

    return login