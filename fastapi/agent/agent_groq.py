import os
import ast
import httpx
from openai import AsyncOpenAI
from agents import function_tool, Agent, Runner, ModelSettings, OpenAIChatCompletionsModel, FunctionTool, set_tracing_disabled
from models import PredictRequestDTO,  PredictFullResponseDTO

set_tracing_disabled(True)

instructions = """
Você é um agente de atendimento ao cliente.

1. Sempre classifique a intenção do usuário utilizando a ferramenta disponível.
2. Utilize a classificação com a mensagem do usuário para retornar a intenção daquela mensagem.
3. Responda de maneira educada e objetiva.
4. Não invente informações.
""" 

def criar_tool_classificar(token: str) -> FunctionTool:

    @function_tool
    async def classificar_intencao(dto: PredictRequestDTO) -> dict:
        """Classifica a intenção de uma mensagem de atendimento."""

        try:
            async with httpx.AsyncClient(verify=False) as client:

                response = await client.post(
                    "https://localhost:8080/predict/classify",
                    json=dto.model_dump(mode="json"),
                    timeout=5,
                    headers={
                        "Authorization": f"Bearer {token}"
                    }
                )

                response.raise_for_status()

                return response.json()

        except Exception as e:
            print("ERRO REAL NA TOOL:", repr(e))
            raise

    return classificar_intencao

def configurar_agent(token: str):
    api_key = os.getenv("GROQ_API_KEY")
    if not api_key:
        raise RuntimeError("GROQ_API_KEY não configurada")

    client = AsyncOpenAI(
        api_key=os.environ["GROQ_API_KEY"],
        base_url="https://api.groq.com/openai/v1"
    )

    model = OpenAIChatCompletionsModel(
        model="openai/gpt-oss-20b",
        openai_client=client
    )

    agent = Agent(
        name="Atendente",
        model=model,
        instructions=instructions,
        tools=[criar_tool_classificar(token)],
        tool_use_behavior="stop_on_first_tool",
        model_settings=ModelSettings(tool_choice="classificar_intencao")
    )
    return agent

async def classificar_groq (dto: PredictRequestDTO, token: str) -> PredictFullResponseDTO:
    agent = configurar_agent(token)
    resposta = await Runner.run(agent, dto.model_dump_json())
    resultado = resposta.final_output

    print('Resultado Final:', resultado)

    if isinstance(resultado, str):
        resultado = ast.literal_eval(resultado)

    return PredictFullResponseDTO.model_validate(resultado)