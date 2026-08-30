from pydantic import BaseModel, Field, ConfigDict, EmailStr
from fastapi import Form


class Predict(BaseModel):
    model_config = ConfigDict(from_attributes=True, extra='forbid')

    id: int = Field(
        description = "Identificador único da mensagem",
        examples = [1]
    )

    text: str  = Field(
        description = "Texto da mensagem",
        examples = ["Quais as formas de pagamento?"]
    )

    intent: str  = Field(
        description = "Intenção da mensagem",
        examples = ["Dúvida"]
    )

    owner_id: int = Field(
        description = "Identificador único do usuário que mandou a mensagem",
        examples = [1]
    )



class PredictRequestDTO(BaseModel):
    model_config = ConfigDict(from_attributes=True, extra='forbid')

    text: str  = Field(
        description = "Texto da mensagem",
        examples = ["Quais as formas de pagamento?"]
    )

    @classmethod
    def as_form( cls, text: str = Form(...)):
        return cls(text = text)


class PredictResponseDTO(BaseModel):
    model_config = ConfigDict(from_attributes=True, extra='forbid')

    id: int = Field(
        description = "Identificador único da mensagem",
        examples = [1]
    )

    text: str  = Field(
        description = "Texto da mensagem",
        examples = ["Quais as formas de pagamento?"]
    )

    intent: str  = Field(
        description = "Intenção da mensagem",
        examples = ["Dúvida"]
    )

    owner_id: int = Field(
        description = "Identificador único do usuário que mandou a mensagem",
        examples = [1]
    )
