import pydantic as pyd
import sqlmodel as sql
from fastapi import Form


class User(sql.SQLModel, table = True):
    __tablename__ = "user"

    id: int = sql.Field(
        description = "Identificador único do usuário",
        primary_key = True
    )

    login: str  = sql.Field(
        description = "Login do usuário"
    )

    name: str  = sql.Field(
        description = "Nome do usuário"
    )

    email: str  = sql.Field(
        description = "Email do usuário"
    )

    hash_password: str  = sql.Field(
        description = "Hash da Senha do usuário"
    )


class UserResponseDTO(pyd.BaseModel):
    model_config = pyd.ConfigDict(from_attributes=True, extra='ignore')

    id: int = pyd.Field(
        description = "Identificador único do usuário",
        examples = [1]
    )

    login: str  = pyd.Field(
        description = "Login do usuário",
        examples = ["usuario.1"]
    )

    name: str  = pyd.Field(
        description = "Nome do usuário",
        examples = ["Usuário 1"]
    )

    email: pyd.EmailStr  = pyd.Field(
        description = "Email do usuário",
        examples = ["email@email.com.br"]
    )


class UserRequestDTO(pyd.BaseModel):
    model_config = pyd.ConfigDict(from_attributes=True, extra='forbid')

    login: str  = pyd.Field(
        description = "Login do usuário",
        examples = ["usuario.1"]
    )

    name: str  = pyd.Field(
        description = "Nome do usuário",
        examples = ["Usuário 1"]
    )

    email: pyd.EmailStr  = pyd.Field(
        description = "Email do usuário",
        examples = ["email@email.com.br"]
    )

    password: str  = pyd.Field(
        description = "Senha do usuário",
        examples = ["strong123Psw!"]
    )

    @classmethod
    def as_form( cls, login: str = Form(...),  name: str = Form(...), email: pyd.EmailStr  = Form(...),  password: str = Form(...) ):
        return cls(login = login, name = name, email = email, password = password )

class UserSignInRequestDTO(pyd.BaseModel):
    model_config = pyd.ConfigDict(from_attributes=True, extra='forbid')

    login: str  = pyd.Field(
        description = "Login do usuário",
        examples = ["usuario.1"]
    )

    password: str  = pyd.Field(
        description = "Senha do usuário",
        examples = ["strong123Psw!"]
    )

    @classmethod
    def as_form( cls, login: str  = Form(...),  password: str = Form(...) ):
        return cls( login = login, password = password )