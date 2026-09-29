import pydantic as pyd
import sqlmodel as sql
from fastapi import Form


class Predict(sql.SQLModel, table = True):
    __tablename__ = "predict"

    id: int = sql.Field(
        description = "Identificador único da mensagem",
        primary_key = True
    )

    text: str  = sql.Field(
        description = "Texto da mensagem"
    )

    intent: str  = sql.Field(
        description = "Intenção da mensagem"
    )

    owner_id: int = sql.Field(
        description = "Identificador único do usuário que mandou a mensagem",
        foreign_key="user.id"
    )


class PredictRequestDTO(pyd.BaseModel):
    model_config = pyd.ConfigDict(from_attributes=True, extra='forbid')

    text: str  = pyd.Field(
        description = "Texto da mensagem",
        examples = ["Quais as formas de pagamento?"]
    )

    @classmethod
    def as_form( cls, text: str = Form(...)):
        return cls(text = text)


class PredictFullResponseDTO(pyd.BaseModel):
    model_config = pyd.ConfigDict(from_attributes=True, extra='ignore')

    id: int = pyd.Field(
        description = "Identificador único da mensagem",
        examples = [1]
    )

    text: str  = pyd.Field(
        description = "Texto da mensagem",
        examples = ["Quais as formas de pagamento?"]
    )

    intent: str  = pyd.Field(
        description = "Intenção da mensagem",
        examples = ["Dúvida"]
    )

    owner_id: int = pyd.Field(
        description = "Identificador único do usuário que mandou a mensagem",
        examples = [1]
    )

class PredictCompactResponseDTO(pyd.BaseModel):
    model_config = pyd.ConfigDict(from_attributes=True, extra='ignore')
    
    text: str  = pyd.Field(
        description = "Texto da mensagem",
        examples = ["Quais as formas de pagamento?"]
    )

    intent: str  = pyd.Field(
        description = "Intenção da mensagem",
        examples = ["Dúvida"]
    )
