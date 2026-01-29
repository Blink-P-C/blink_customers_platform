# Blink Customers Platform

Portal do cliente para consultoria e projetos, desenvolvido pela Blink Projects & Consulting.

🔗 **Repositório**: https://github.com/Blink-P-C/blink_customers_platform

## 🚀 Setup Rápido

```bash
git clone https://github.com/Blink-P-C/blink_customers_platform.git
cd blink_customers_platform
./setup.sh
```

Acesse: http://localhost:3000 (lincoln.oliver@blinkpec.com / WEV7ui8YB3ay1v21)

📖 **Ver guia completo**: [QUICKSTART.md](QUICKSTART.md)

## 🚀 Tecnologias

### Backend
- **Python 3.11+** com FastAPI
- **PostgreSQL** como banco de dados
- **SQLAlchemy** + **Alembic** para ORM e migrations
- **Microsoft SharePoint** (via Graph API) para armazenamento de arquivos e vídeos
- **Google Calendar API** para agendamento de aulas
- **JWT** para autenticação (bcrypt para hashing de senhas)

### Frontend
- **Next.js 14** (App Router)
- **TypeScript**
- **Tailwind CSS** para estilização
- **Zustand** para gerenciamento de estado
- **Axios** para requisições HTTP

## 📦 Features

### 1. Autenticação e RBAC
- Login com email/senha
- Tokens JWT (access + refresh)
- Roles: **admin** e **client**
- Admin gerencia tudo; client vê apenas seus projetos

### 2. Projetos
- CRUD de projetos (admin)
- Associar clientes a projetos
- Dashboard mostra projetos do cliente

### 3. Gravações (Aulas/Consultorias)
- Admin faz upload de vídeos → SharePoint
- Cliente vê gravações do seu projeto
- Download/streaming via SharePoint

### 4. Agendamento de Aulas
- Admin define slots de disponibilidade
- Cliente reserva horários
- Integração com Google Calendar (cria evento automaticamente)
- Link da reunião (Google Meet)

### 5. Arquivos de Projeto
- Upload de arquivos → SharePoint
- Download de arquivos do projeto
- Organização por projeto

### 6. Solicitações (Melhorias/Revisões)
- Cliente cria solicitações (título, descrição, tipo)
- Admin responde e altera status
- Histórico de mensagens por solicitação

### 7. Dashboard Admin
- Visão geral: projetos, clientes, solicitações pendentes
- Próximas aulas agendadas

## 🛠️ Setup

### Pré-requisitos
- Docker e Docker Compose
- Node.js 20+ (para desenvolvimento local)
- Python 3.11+ (para desenvolvimento local)

### 1. Clone o repositório
```bash
git clone https://github.com/Blink-P-C/blink_customers_platform.git
cd blink_customers_platform
```

### 2. Configure as variáveis de ambiente
```bash
cp .env.example .env
```

Edite o `.env` e preencha:
- `SECRET_KEY`: Gere uma chave secreta forte
- Credenciais do **Microsoft Graph API** (SharePoint)
- Credenciais do **Google Calendar API**

#### Como obter credenciais da Microsoft (SharePoint)
1. Acesse o [Azure Portal](https://portal.azure.com)
2. Crie um **App Registration**
3. Configure permissões: `Files.ReadWrite.All`, `Sites.ReadWrite.All`
4. Crie um **client secret**
5. Obtenha o **Tenant ID**, **Client ID**, **Site ID** e **Drive ID**

#### Como obter credenciais do Google Calendar
1. Acesse o [Google Cloud Console](https://console.cloud.google.com)
2. Crie um projeto
3. Habilite a **Google Calendar API**
4. Crie credenciais **OAuth 2.0**
5. Configure o redirect URI: `http://localhost:8000/auth/google/callback`

### 3. Inicie os serviços com Docker Compose
```bash
docker-compose up --build
```

Isso irá:
- Criar o banco de dados PostgreSQL
- Rodar as migrations do Alembic
- Iniciar o backend FastAPI na porta **8000**
- Iniciar o frontend Next.js na porta **3000**

### 4. Acesse a aplicação
- **Frontend**: http://localhost:3000
- **Backend API**: http://localhost:8000
- **Documentação da API**: http://localhost:8000/docs

### 5. Criar primeiro usuário admin
Execute no container do backend:
```bash
docker-compose exec backend python -c "
from app.database import SessionLocal
from app.models.user import User, UserRole
from app.utils.security import get_password_hash

db = SessionLocal()
admin = User(
    email='lincoln.oliver@blinkpec.com',
    hashed_password=get_password_hash('WEV7ui8YB3ay1v21'),
    full_name='Administrador',
    role=UserRole.ADMIN
)
db.add(admin)
db.commit()
print('Admin criado: lincoln.oliver@blinkpec.com / WEV7ui8YB3ay1v21')
"
```

## 🔧 Desenvolvimento Local

### Backend
```bash
cd backend
python -m venv venv
source venv/bin/activate  # Linux/Mac
# ou: venv\Scripts\activate  # Windows
pip install -r requirements.txt
alembic upgrade head
uvicorn app.main:app --reload
```

### Frontend
```bash
cd frontend
npm install
npm run dev
```

## 📁 Estrutura do Projeto

```
blink_customers_platform/
├── backend/
│   ├── app/
│   │   ├── main.py                 # FastAPI app
│   │   ├── config.py               # Configurações
│   │   ├── database.py             # Database setup
│   │   ├── models/                 # SQLAlchemy models
│   │   ├── schemas/                # Pydantic schemas
│   │   ├── routers/                # API routes
│   │   ├── services/               # SharePoint, Google Calendar
│   │   └── utils/                  # Security, dependencies
│   ├── alembic/                    # Database migrations
│   ├── requirements.txt
│   └── Dockerfile
├── frontend/
│   ├── src/
│   │   ├── app/                    # Next.js pages (App Router)
│   │   ├── components/             # React components
│   │   ├── lib/                    # API client, auth, types
│   │   └── styles/                 # CSS global
│   ├── package.json
│   ├── next.config.js
│   ├── tailwind.config.ts
│   └── Dockerfile
├── docker-compose.yml
├── .env.example
└── README.md
```

## 🔐 Segurança

- Senhas hashadas com **bcrypt**
- JWT com tokens de refresh
- CORS configurado
- Validação de permissões (RBAC)
- SQL Injection protegido pelo SQLAlchemy

## 📝 API Endpoints

### Auth
- `POST /auth/register` - Registrar usuário
- `POST /auth/login` - Login
- `POST /auth/refresh` - Refresh token
- `GET /auth/me` - Obter usuário atual

### Projects
- `GET /projects` - Listar projetos
- `POST /projects` - Criar projeto (admin)
- `GET /projects/{id}` - Detalhes do projeto
- `PUT /projects/{id}` - Atualizar projeto (admin)
- `DELETE /projects/{id}` - Deletar projeto (admin)

### Recordings
- `GET /recordings` - Listar gravações
- `POST /recordings` - Upload de gravação (admin)
- `GET /recordings/{id}` - Detalhes da gravação
- `GET /recordings/{id}/download-url` - Link de download
- `DELETE /recordings/{id}` - Deletar gravação (admin)

### Bookings
- `GET /bookings` - Listar agendamentos
- `POST /bookings` - Criar agendamento
- `GET /bookings/slots` - Listar slots disponíveis
- `POST /bookings/slots` - Criar slot (admin)
- `DELETE /bookings/{id}` - Cancelar agendamento

### Files
- `GET /files` - Listar arquivos
- `POST /files` - Upload de arquivo (admin)
- `GET /files/{id}/download-url` - Link de download
- `DELETE /files/{id}` - Deletar arquivo (admin)

### Requests
- `GET /requests` - Listar solicitações
- `POST /requests` - Criar solicitação
- `GET /requests/{id}` - Detalhes da solicitação
- `PUT /requests/{id}` - Atualizar solicitação
- `POST /requests/{id}/messages` - Adicionar mensagem
- `GET /requests/{id}/messages` - Listar mensagens

## 🤝 Contribuindo

1. Faça um fork do projeto
2. Crie uma branch para sua feature (`git checkout -b feature/AmazingFeature`)
3. Commit suas mudanças (`git commit -m 'Add some AmazingFeature'`)
4. Push para a branch (`git push origin feature/AmazingFeature`)
5. Abra um Pull Request

## 📄 Licença

Este projeto é privado e pertence à **Blink Projects & Consulting**.

## 👥 Autores

- **Blink Projects & Consulting** - [GitHub](https://github.com/Blink-P-C)

## 📞 Suporte

Para suporte, entre em contato: contato@blinkpec.com
