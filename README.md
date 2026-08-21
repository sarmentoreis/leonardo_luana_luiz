# leonardo_luana_luiz
Projeto de Bloco: Análise e Segurança de Agentes de IA.

## Diretório Data
Diretório onde está o arquivo .csv utilizado como dataset .

## Diretório EDA
Diretório onde está o arquivo .ipynb da Analise Exploratória de Dados (EDA) feita com base no arquivo .csv do diretório data.

## Diretório Others
Diretório onde se encontram arquivos diversos produzidos nesse trabalho, como por exemplo o arquivo do diagrama de fluxo de dados (DFD).

## Diretório FastAPI
Diretório onde se encontram os arquivos do código fonte da aplicação Python utilizando FastAPI.

### Diretório Datas
Diretório onde se encontram os arquivos de repositório da FastAPI. Será o repositório onde ocorrerá o acesso aos dados.

### Diretório Models
Diretório onde se encontram os arquivos de modelos das entidades do banco de dados, além de classes DTO relacionadas a essas entidades.

### Diretório Routes
Diretório onde se encontram os arquivos de rotas da aplicação, separados por entidade relacionadas.

### Diretório Security
Diretório onde se encontram os métodos e configurações relacionadas com o JWT e OAuth2

### Arquivo Requirements.txt
Lista das bibliotecas utilizadas.


### Guia de utilização
- Acesse a pasta desse repositório, e acesse a pasta do fastapi.
- Crie uma venv para o projeto com o comando: python -m venv venv
- Ative esse venv utilizando um dos comandos abaixo:
    - PowerShell: .\venv\Scripts\Activate.ps1  
    - CMD: venv\Scripts\activate
    - Linux: source venv/bin/activate
- Instale as dependências do projeto com: python -m pip install -r requirements.txt
- Para executar o projeto de FastAPI é só necessário executar o arquivo main.py na raiz desse projeto, ele já conta com os comandos de inicialização do servidor para serem executados via código.
