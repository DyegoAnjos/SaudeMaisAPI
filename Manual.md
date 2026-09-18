# Saude+ API

API do projeto Saude+, desenvolvida em Python com FastAPI, SQLAlchemy e Alembic[cite: 1].

---

## 🛠️ Pré-requisitos

Antes de começar, certifique-se de ter as seguintes ferramentas instaladas no seu sistema:

* **Python 3.14 ou superior:** [Download do Python](https://www.python.org/downloads/)
* **Git:** Para clonar o repositório. [Download do Git](https://git-scm.com/downloads)
* **Windows PowerShell** (ou terminal Bash/Linux/Mac)

### Como baixar o projeto

Abra o seu terminal e rode o comando para clonar o repositório:

```powershell
git clone [https://github.com/dyegoanjos/saudemaisapi.git](https://github.com/dyegoanjos/saudemaisapi.git)
cd saudemaisapi
```

---

## 🚀 Rodar o Projeto

Siga os passos abaixo para preparar o ambiente virtual e colocar a API para funcionar:

### 1. Criar e ativar o ambiente virtual

No terminal, dentro da pasta do projeto, crie o ambiente virtual `.venv`:

```powershell
py -3.14 -m venv .venv
```

Em seguida, ative o ambiente virtual:

```powershell
.\.venv\Scripts\Activate.ps1
```

> 💡 **Nota (Windows):** Se o PowerShell bloquear a ativação, rode o comando abaixo uma vez como Administrador para liberar a execução de scripts:
> 
> ```powershell
> Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
> ```

### 2. Instalar as dependências

Com o ambiente virtual ativado, instale os pacotes do projeto:

```powershell
python -m pip install --group dev -e .
```

### 3. Configurar variáveis de ambiente e pastas

Crie o arquivo `.env` na raiz do projeto contendo a URL da base de dados:

```env
DATABASE_URL=sqlite+aiosqlite:///./saudemais.db
```

Crie a pasta de `uploads` para o armazenamento de imagens:

```powershell
mkdir uploads
```

Execute as migrações do banco de dados (Alembic):

```powershell
alembic upgrade head
```

### 4. Iniciar a API

Para colocar o servidor de desenvolvimento a rodar, utilize o atalho do Task:

```powershell
task run
```

*(Caso não utilize o Task, pode rodar diretamente com `fastapi dev saudemaisapi/app.py`)*

Pronto! A API estará disponível em:

* **Verificação de status:** http://127.0.0.1:8000/
* **Documentação Swagger UI:** http://127.0.0.1:8000/docs
