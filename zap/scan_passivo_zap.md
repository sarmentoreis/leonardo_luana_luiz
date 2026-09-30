## EXEMPLO 01 — Credenciais de Autenticação Capturadas

**Finding:** Credenciais de Autenticação Capturadas  
**Severidade:** HIGH  
**Confiança:** MEDIUM  
**URL Afetada:** [http://localhost:8080/auth/token](http://localhost:8080/auth/token)

### O que foi detectado

O OWASP ZAP identificou que estamos utilizando HTTP na API e, com isso, obteve acesso às credenciais do usuário.

### Por que é um problema

Possibilita que os atacantes tenham acesso aos dados trafegados na API sem que exista nenhuma criptografia na troca de mensagens, em especial na API de autenticação.

### Correção realizada

A correção proposta seria implementar a utilização de HTTPS na API, para que as trocas de mensagens sejam criptografadas. Esse ajuste ainda não foi realizado.

### Validação

A validação seria realizada utilizando o scan passivo do OWASP ZAP novamente e verificando que as mensagens estão protegidas pela criptografia do HTTPS.

### Risco aceito, se não corrigido

O ajuste ainda não foi realizado, pois estamos em etapa de desenvolvimento. A aplicação ainda não está pronta para homologação ou produção.

## EXEMPLO 02 — Content Security Policy (CSP) Header Not Set

**Finding:** Content Security Policy (CSP) Header Not Set  
**Severidade:** MEDIUM  
**Confiança:** HIGH  
**URL Afetada:** [http://localhost:8080/docs](http://localhost:8080/docs)

### O que foi detectado

O OWASP ZAP identificou que a resposta HTTP do endpoint `/docs` não possui o header `Content-Security-Policy` (CSP).

### Por que é um problema

Sem uma política CSP, o navegador não possui restrições explícitas sobre quais origens podem fornecer scripts, estilos, imagens e outros conteúdos.

Isso reduz a proteção contra ataques como Cross-Site Scripting (XSS) e a injeção de conteúdo malicioso.

### Correção realizada

Foi adicionado o header CSP no middleware da aplicação FastAPI:

```python
response.headers["Content-Security-Policy"] = (
    "default-src 'self'; "
    "script-src 'self' https://cdn.jsdelivr.net 'unsafe-inline'; "
    "style-src 'self' https://cdn.jsdelivr.net 'unsafe-inline'; "
    "img-src 'self' data: https://fastapi.tiangolo.com; "
    "font-src 'self' https://cdn.jsdelivr.net; "
    "connect-src 'self' https://cdn.jsdelivr.net;"
)
```
### Validação

A validação seria realizada utilizando o scan passivo do OWASP ZAP novamente e verificando se os alertas referentes a essa vulnerabilidade desapareceram.

### Risco aceito, se não corrigido

Não se aplica, pois a correção foi realizada.

## EXEMPLO 03 — Sub Resource Integrity Attribute Missing

**Finding:** Sub Resource Integrity Attribute Missing  
**Severidade:** MEDIUM  
**Confiança:** HIGH  
**URL Afetada:** [http://localhost:8080/docs](http://localhost:8080/docs)

### O que foi detectado

O OWASP ZAP identificou que scripts externos estão sendo utilizados sem o atributo de integridade (*Subresource Integrity* — SRI).

### Por que é um problema

Caso um atacante obtenha controle desse serviço externo, ele poderia injetar conteúdo malicioso na aplicação.

### Correção realizada

Caso o script externo tivesse sido utilizado diretamente no código da aplicação, deveríamos utilizar um atributo de validação da integridade do conteúdo desse script.

Porém, como se trata de um arquivo utilizado pelo Swagger, não conseguimos alterar essas configurações.

### Validação

A validação seria realizada utilizando o scan passivo do OWASP ZAP novamente e verificando se os alertas referentes a essa vulnerabilidade desapareceram.

### Risco aceito, se não corrigido

Aceitamos o risco, pois se trata de um script externo utilizado pelo Swagger e não temos acesso para alterar as configurações dessa importação.