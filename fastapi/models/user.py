from pydantic import BaseModel, Field, ConfigDict, EmailStr
from fastapi import Form


class User(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int = Field(
        description = "Identificador único do usuário",
        examples = [1]
    )

    login: str  = Field(
        description = "Login do usuário",
        examples = ["usuario.1"]
    )

    name: str  = Field(
        description = "Nome do usuário",
        examples = ["Usuário 1"]
    )

    email: EmailStr  = Field(
        description = "Email do usuário",
        examples = ["email@email.com.br"]
    )

    password: str  = Field(
        description = "Senha do usuário",
        examples = ["strong123Psw!"]
    )

    audit_token: str  = Field(
            description = "Token de auditoria",
            examples = ["550e8400-e29b-41d4-a716-446655440000"]
    )


class UserResponseDTO(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int = Field(
        description = "Identificador único do usuário",
        examples = [1]
    )

    login: str  = Field(
        description = "Login do usuário",
        examples = ["usuario.1"]
    )

    name: str  = Field(
        description = "Nome do usuário",
        examples = ["Usuário 1"]
    )

    email: EmailStr  = Field(
        description = "Email do usuário",
        examples = ["email@email.com.br"]
    )


class UserRequestDTO(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    name: str  = Field(
        description = "Nome do usuário",
        examples = ["Usuário 1"]
    )

    email: EmailStr  = Field(
        description = "Email do usuário",
        examples = ["email@email.com.br"]
    )

    password: str  = Field(
        description = "Senha do usuário",
        examples = ["strong123Psw!"]
    )

    @classmethod
    def as_form( cls, login: str = Form(...),  name: str = Form(...), email: EmailStr  = Form(...),  password: str = Form(...) ):
        return cls(login = login, name = name, email = email, password = password )

class UserSignInRequestDTO(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    login: str  = Field(
        description = "Login do usuário",
        examples = ["usuario.1"]
    )

    password: str  = Field(
        description = "Senha do usuário",
        examples = ["strong123Psw!"]
    )

    @classmethod
    def as_form( cls, login: str  = Form(...),  password: str = Form(...) ):
        return cls( login = login, password = password )