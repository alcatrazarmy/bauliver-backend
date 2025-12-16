# Bauliver Backend

The Bauliver Backend powers the Bauliver Operating System — an infrastructure layer designed to manage permits, inspections, workflows, billing logic, contractor operations, and solar-related data automation.
This system is engineered for scalability, automation, and speed, supporting both internal teams and external partners.

## 🤖 NEW: Autonomous Bot System

**Bauliver now includes a fully autonomous bot system that demonstrates real-world automation capabilities!**

The autonomous bot can:
- **Process permits automatically** - Submit and track permit applications without human intervention
- **Automate entire projects** - From lead qualification to installation scheduling
- **Execute complex workflows** - Multi-step automation for construction and solar projects
- **Demonstrate real autonomy** - See freedom through automation in action

[**📖 View the Complete Autonomous Bot Guide →**](./AUTONOMOUS_BOT_GUIDE.md)

## 🏗️ Tech Stack

| Layer | Technology |
|-------|-----------|
| Language | Python 3.11+ |
| Framework | FastAPI |
| ORM / Migrations | SQLAlchemy + Alembic |
| Database | PostgreSQL / SQLite |
| Authentication | JWT (python-jose) |
| CI/CD | GitHub Actions |
| Packaging | pip |

## ✨ Core Features

✅ **Autonomous Bot System** - NEW! Full automation capabilities
- Permit processing automation
- Project workflow automation  
- Task execution and tracking
- Workflow creation and management

✅ **Authentication & Authorization**
- User registration and login
- JWT-based authentication
- Role-based access control

✅ **Core Infrastructure** (Planned)
- Permit management engine
- Contractor onboarding + credential management
- Billing logic (Solar Bot Bill Reader integration)
- Document processing
- API endpoints for Bauliver OS UI

## 📁 Project Structure

```
bauliver-backend/
│
├── app/
│   ├── core/              # Security, config, utilities
│   ├── routers/           # API routes (auth, bot, etc.)
│   ├── models.py          # Database models
│   ├── schemas.py         # Pydantic schemas
│   ├── database.py        # Database connection
│   └── main.py            # Application entry point
│
├── migrations/            # Alembic migrations
│   └── versions/          # Migration files
├── .github/workflows/     # CI/CD pipelines
├── alembic.ini           # Migration settings
├── requirements.txt       # Python dependencies
├── README.md             # This file
└── AUTONOMOUS_BOT_GUIDE.md  # Autonomous bot documentation
```

🚀 Getting Started
1. Clone the Repository
git clone https://github.com/alcatrazarmy/bauliver-backend.git
cd bauliver-backend

2. Create & Activate Virtual Environment
python -m venv venv
source venv/bin/activate     # macOS/Linux
venv\Scripts\activate        # Windows

3. Install Dependencies
pip install -r requirements.txt


(Or I’ll rewrite this if you're using Poetry.)

🔧 Environment Variables

Create a .env file in the project root:

DATABASE_URL=postgresql://user:password@localhost:5432/bauliver
SECRET_KEY=your-secret-key
ENV=development

🗄️ Database Migrations

Run migrations:

alembic upgrade head


Create new migration:

alembic revision --autogenerate -m "description"

▶️ Running the App
uvicorn app.main:app --reload


The server will start at:
http://localhost:8000

🧪 Running Tests
pytest

🔄 CI/CD Pipeline

GitHub Actions automatically:

Runs tests

Validates migrations

Ensures code quality

Add badges here once pipeline is finalized.

📚 Documentation Roadmap

This repo will eventually include:

Full API reference

Database schema diagrams

System workflow diagrams

Developer onboarding guide

Integration notes for Solar Bot & external services

🛠️ Contribution Guidelines

Create a new branch for each feature.

Submit PRs with clear descriptions.

Ensure all tests pass before requesting review.

Maintain clean commits — your future self will thank you.

🧠 Project Vision

Bauliver is designed to bring clarity, efficiency, and automation to construction + solar + permitting operations.
This backend is the engine that makes the ecosystem run.

## 🤖 Quick Start: Autonomous Bot Demo

See the autonomous bot in action:

```bash
# 1. Start the server
uvicorn app.main:app --reload

# 2. Register a user
curl -X POST http://localhost:8000/auth/register \
  -H "Content-Type: application/json" \
  -d '{"email":"demo@example.com","password":"demo123","role":"admin"}'

# 3. Login to get token
curl -X POST http://localhost:8000/auth/login \
  -d "username=demo@example.com&password=demo123"

# 4. Run the autonomous demo (use your token from step 3)
curl -X POST http://localhost:8000/bot/demo/build-automation \
  -H "Authorization: Bearer YOUR_TOKEN_HERE"
```

[**📖 Full Autonomous Bot Guide →**](./AUTONOMOUS_BOT_GUIDE.md)

## 📚 API Endpoints Summary

### Public Endpoints
- `GET /` - API information
- `GET /health` - Health check
- `GET /bot/status` - Bot system status

### Authentication (`/auth`)
- `POST /auth/register` - Register new user
- `POST /auth/login` - Login and get JWT token
- `GET /auth/me` - Get current user info

### Autonomous Bot (`/bot`) - Requires Authentication
- `POST /bot/tasks` - Create autonomous task
- `GET /bot/tasks` - List tasks
- `POST /bot/tasks/{id}/execute` - Execute task autonomously
- `POST /bot/workflows` - Create workflow
- `GET /bot/workflows` - List workflows
- `POST /bot/demo/build-automation` - **Demo autonomous building in real-life**

---

**This is real autonomous building. This is freedom through automation. This is Bauliver.**
