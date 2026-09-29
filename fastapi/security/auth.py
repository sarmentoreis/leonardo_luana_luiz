import jwt
from jwt.exceptions import InvalidTokenError
from datetime import datetime, timezone, timedelta
from models import User
from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from consts.roles_permissions import ROLE_PERMISSIONS
from models.token_data import TokenData

SECRET_KEY = "MinhaChaveSecretaJWT2026_ABC123!"
TOKEN_DURATION_MINUTES = 30
TOKEN_ALGORITHM = "HS256"
TOKEN_URL = "/auth/token"
TOKEN_TYPE = "Bearer"

oauth2_scheme = OAuth2PasswordBearer(tokenUrl=TOKEN_URL)

def create_token(user: User) -> str:
    expiracao = datetime.now(timezone.utc) + timedelta(minutes=30)
    iat = datetime.now(timezone.utc)
    dados = {
        "sub": str(user.id),
        "exp": expiracao,
        "iat": iat,
        "permissions": ROLE_PERMISSIONS.get(user.role, []),
        "role": user.role,
    }
    token = jwt.encode(payload = dados, key = SECRET_KEY, algorithm = TOKEN_ALGORITHM)
    return token

def create_token_return(user: User):
    token = create_token(user = user)
    return {
        "access_token": token,
        "token_type": TOKEN_TYPE
    }

def validate_token(token: str = Depends(oauth2_scheme)) -> TokenData:
    error = HTTPException(
        status_code=401,
        detail="Token inválido ou expirado",
        headers={"WWW-Authenticate": TOKEN_TYPE}
    )

    try:
        result = jwt.decode(jwt = token, key = SECRET_KEY, algorithms = [TOKEN_ALGORITHM])

        if result is None:
            raise error

        expiration = result.get('exp')
        if expiration is None :            
            raise error

        expiration = datetime.fromtimestamp(
            expiration,
            tz=timezone.utc
        )

        if expiration < datetime.now(timezone.utc):
            raise error    

        entity_id = result.get('sub')
        permissions = result.get('permissions')
        role = result.get('role')

        if entity_id is None:
            raise error

        token_data = TokenData(entity_id = int(entity_id), permissions = permissions, role = role)
        
    except InvalidTokenError:
        raise error

    return token_data