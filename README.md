# Saude+ API

API do projeto Saude+, desenvolvida com FastAPI, SQLAlchemy e Alembic.

## Requisitos

- Python 3.14 ou superior
- Windows PowerShell

## Preparar o projeto pela primeira vez

Abra o PowerShell na pasta do projeto e crie um ambiente virtual:

```powershell
py -3.14 -m venv .venv
```

Ative o ambiente virtual:

```powershell
.\.venv\Scripts\Activate.ps1
```

Instale o projeto e suas dependencias:

```powershell
python -m pip install --group dev -e .
```

## Configurar o banco de dados

O arquivo `.env` deve existir na raiz do projeto com o seguinte conteudo para
usar um banco SQLite local:

```env
DATABASE_URL=sqlite+aiosqlite:///./saudemais.db
```

Crie ou atualize as tabelas do banco:

```powershell
alembic upgrade head
```

## Iniciar a API

Com o ambiente virtual ativado, execute:

```powershell
fastapi dev saudemaisapi/app.py
```

Depois, acesse:

- Verificacao da API: http://127.0.0.1:8000/
- Documentacao interativa: http://127.0.0.1:8000/docs

Durante o desenvolvimento, a API aceita requisicoes de fronts locais nas
portas `3000` e `5173`, usando `localhost` ou `127.0.0.1`.

A rota inicial deve responder:

```json
{
  "mensagem": "API Saude+ funcionando"
}
```

## Executar os testes

```powershell
pytest
```

O Pytest executa automaticamente funcoes cujo nome comeca com `test`. Para
confirmar quais testes foram encontrados sem executa-los, use:

```powershell
pytest --collect-only
```

## Estrutura principal

- `saudemaisapi/app.py`: cria a aplicacao e registra as rotas.
- `saudemaisapi/models.py`: define as tabelas do banco.
- `saudemaisapi/schemas.py`: define os dados recebidos e devolvidos pela API.
- `saudemaisapi/routers/`: contem as rotas de cada recurso.
- `migrations/`: contem o historico de alteracoes do banco.
- `tests/`: contem os testes automatizados.

## Rotas de categorias e unidades de saude

As duas funcionalidades oferecem as operacoes completas de cadastro:

- `GET /categorias/` e `GET /unidades-saude/`: listar.
- `GET /categorias/{id}` e `GET /unidades-saude/{id}`: buscar por ID.
- `POST /categorias/` e `POST /unidades-saude/`: criar.
- `PUT /categorias/{id}` e `PUT /unidades-saude/{id}`: atualizar.
- `DELETE /categorias/{id}` e `DELETE /unidades-saude/{id}`: remover.

## Validacoes principais

- Nota de comentario: entre 0 e 5.
- Capacidade maxima de evento: maior que zero, quando informada.
- Data final do evento: nao pode ser anterior a data inicial.
- Paginacao: `limit` entre 1 e 100 e `offset` maior ou igual a zero.
- Coordenadas: latitude entre -90 e 90 e longitude entre -180 e 180.
- Lotacao e tempo medio de atendimento: nao podem ser negativos.

## Fotografias

As fotografias sao enviadas como `multipart/form-data`. A API aceita imagens
JPEG, PNG e WebP com tamanho maximo de 5 MB. O arquivo e salvo na pasta
`uploads/` com um nome unico, enquanto o banco guarda o caminho, o nome
original, o tipo e o tamanho.

- `POST /fotografias/criar_fotografia`: enviar uma imagem.
- `GET /fotografias/{id}`: consultar os metadados.
- `GET /fotografias/{id}/arquivo`: baixar ou exibir a imagem.
- `PUT /fotografias/atualizar_fotografia/{id}`: trocar a imagem.
- `DELETE /fotografias/remover_fotografia/{id}`: remover a imagem.

## Observacao de seguranca

O arquivo `.env` pode conter dados privados e nao deve ser enviado ao GitHub.
Ele ja esta listado no `.gitignore` deste projeto.
