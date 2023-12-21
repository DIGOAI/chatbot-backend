[![Apply migrations to dev DB if migrations folder changed](https://github.com/DIGOAI/chatbot-backend/actions/workflows/migrate_db.yml/badge.svg)](https://github.com/DIGOAI/chatbot-backend/actions/workflows/migrate_db.yml)

### 🤖💬 Chatbot
Backend API, for managing some business logic related of an internet provider called `SARAGUROS NET`. 

### ⛏️ Technologies
- FastAPI
- Alembic
- Postgres

### ⚙️ Installation
the project uses pipenv, so you can create a virtual environment, and install the dependencies as follow:

```bash
# Set and activate the virtual environment
python -m venv venv
source venv/bin/activate

# install the dependencies
pipenv install
```

### ⚡️ Development
```bash
uvicorn main:app --host 0.0.0.0 --port 8000 --reload
```
