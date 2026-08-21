## **1. Cliente Externo (Usuário)**

| CIA                   | Aplicação                                                                            |
| --------------------- | ------------------------------------------------------------------------------------ |
| **Confidencialidade** | Credenciais e JWT não devem ser expostos                                             |
| **Integridade**       | Todas as requisições devem conter tokens JWT em seu cabeçalho                        |
| **Disponibilidade**   | API deve permanecer acessível para os usuários através da internet (domínio público) |

---

## **2. FastAPI App**

| CIA                   | Aplicação                                                                                                    |
| --------------------- | ------------------------------------------------------------------------------------------------------------ |
| **Confidencialidade** | Necessário aplicação de autenticação JWT em todas as rotas protegidas e comunicação por meio de HTTPS        |
| **Integridade**       | Necessária a aplicação de autorização por meio de roles para proteção de funcionalidades sensíveis           |
| **Disponibilidade**   | Necessário a API estar em ambiente de produção/staging, como containers/nuvens para garantir disponibilidade |

---

## **3. Banco de Dados**

| CIA                   | Aplicação                                                                       |
| --------------------- | ------------------------------------------------------------------------------- |
| **Confidencialidade** | Informações sensíveis são salvas em **texto puro**                              |
| **Integridade**       | Necessário aplicar controle de race conditions no salvamento de dados           |
| **Disponibilidade**   | Não existe um banco de dados implementado para retenção dos dados entre sessões |
