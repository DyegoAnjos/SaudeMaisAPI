# Saude+ API

API do projeto Saude+, desenvolvida com **FastAPI**, **SQLAlchemy** e **Alembic** para gerenciamento de eventos, categorias, unidades de saúde e fotografias.

---

## 🛠️ Requisitos

* **Python:** 3.14 ou superior
* **Sistema Operacional:** Windows PowerShell (ou terminal Bash/Linux/Mac)

---

## 🚀 Preparar o projeto pela primeira vez

1. **Abra o terminal na pasta raiz do projeto** e crie um ambiente virtual:
   
   ```powershell
   py -3.14 -m venv .venv
   ```

2. **Ative o ambiente virtual:**
   
   ```powershell
   .\.venv\Scripts\Activate.ps1
   ```
   
   > 💡 **Nota de permissão:** Se o PowerShell exibir um erro de execução de scripts, rode o comando abaixo uma única vez no terminal como Administrador:
   > 
   > ```powershell
   > Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
   > ```

3. **Instale o projeto e suas dependências de desenvolvimento:**
   
   ```powershell
   python -m pip install --group dev -e .
   ```

---

## ⚙️ Configurar o ambiente e o banco de dados

1. **Crie um arquivo `.env` na raiz do projeto** com o seguinte conteúdo para utilizar o banco SQLite local:
   
   ```env
   DATABASE_URL=sqlite+aiosqlite:///./saudemais.db
   ```

2. **Crie a pasta de uploads** para o armazenamento local das fotos enviadas pela API:
   
   ```powershell
   mkdir uploads
   ```

3. **Crie ou atualize as tabelas do banco de dados via Alembic:**
   
   ```powershell
   alembic upgrade head
   ```

---

## 💻 Iniciar a API

Com o ambiente virtual ativado, execute o servidor de desenvolvimento:

```powershell
fastapi dev saudemaisapi/app.py
```

Acesse no seu navegador:

* **Verificação de status:** [http://127.0.0.1:8000/](http://127.0.0.1:8000/)
* **Documentação interativa (Swagger UI):** [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)

*Durante o desenvolvimento, a API aceita requisições de front-ends locais nas portas `3000` e `5173` (`localhost` ou `127.0.0.1`).*

A rota inicial (`GET /`) deve responder:

```json
{
  "mensagem": "API Saude+ funcionando"
}
```

---

## 🌐 Expor a API com o ngrok (Opcional)

Para testar a API com aplicações externas ou mobile via túnel público:

1. **Inicie o servidor local na porta 8000:**
   
   ```powershell
   fastapi dev saudemaisapi/app.py
   ```
2. **Em outro terminal, abra o túnel ngrok:**
   
   ```powershell
   ngrok http 8000
   ```
3. **Acesse a documentação remota:** `https://<seu-subdominio>.ngrok-free.app/docs`

---

## 🧪 Executar os testes automatizados

Para rodar a suíte completa de testes com o **Pytest**:

```powershell
pytest
```

Para apenas listar quais testes foram encontrados sem executá-los:

```powershell
pytest --collect-only
```

---

## 📂 Estrutura do Projeto

```text
SaudeMaisAPI/
├── saudemaisapi/
│   ├── app.py              # Instância principal do FastAPI e inclusão de roteadores
│   ├── models.py           # Modelos de tabelas do banco de dados (SQLAlchemy)
│   ├── schemas.py          # Schemas e validações de dados (Pydantic)
│   └── routers/            # Endpoints segregados por recurso (eventos, fotografias, etc.)
├── migrations/             # Histórico de migrações da base de dados (Alembic)
├── uploads/                # Armazenamento de arquivos estáticos de imagem
├── tests/                  # Testes unitários e de integração (Pytest)
├── alembic.ini             # Arquivo de configuração do Alembic
└── pyproject.toml          # Gerenciamento de dependências e metadados
```

---

## 📌 Principais Regras e Validações

* **Nota de comentário:** Valor numérico entre 0 e 5.
* **Capacidade máxima de evento:** Maior que zero (`gt=0`), quando informada.
* **Data do evento:** A data de fim não pode ser anterior à data de início.
* **Paginação:** `limit` entre 1 e 100 e `offset` maior ou igual a zero.
* **Coordenadas geográficas:** Latitude entre -90 e 90, e longitude entre -180 e 180.
* **Lotação e tempo médio:** Não aceitam valores negativos.

---

## 🖼️ Módulo de Fotografias

As imagens são enviadas como `multipart/form-data` (formatos aceitos: JPEG, PNG e WebP; tamanho máximo de 5 MB). O arquivo físico é salvo na pasta `uploads/` com UUID único, e seus metadados são salvos no banco.

* `POST /fotografias/criar_fotografia`: Enviar uma imagem.
* `GET /fotografias/{id}`: Consultar metadados.
* `GET /fotografias/{id}/arquivo`: Baixar ou visualizar a imagem.
* `PUT /fotografias/atualizar_fotografia/{id}`: Substituir a imagem.
* `DELETE /fotografias/remover_fotografia/{id}`: Excluir a imagem.

---

## 🔒 Segurança

O arquivo `.env` pode conter dados sensíveis e **nunca deve ser commitado** no repositório (já configurado no `.gitignore`).
