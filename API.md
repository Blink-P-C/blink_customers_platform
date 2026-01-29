# API Documentation

Documentação completa da API do Blink Customers Platform.

**Base URL**: `http://localhost:8000`

**Documentação Interativa**: http://localhost:8000/docs (Swagger UI)

## Autenticação

A API usa **JWT Bearer Token** para autenticação.

### Obter Token

```http
POST /auth/login
Content-Type: multipart/form-data

username=seu@email.com&password=suasenha
```

**Response:**
```json
{
  "access_token": "eyJhbGc...",
  "refresh_token": "eyJhbGc...",
  "token_type": "bearer"
}
```

### Usar Token

Inclua o token no header de todas as requisições autenticadas:

```http
Authorization: Bearer eyJhbGc...
```

## Endpoints

### 🔐 Authentication

#### Register
```http
POST /auth/register
Content-Type: application/json

{
  "email": "novo@email.com",
  "password": "senha123",
  "full_name": "Nome Completo",
  "role": "client"
}
```

#### Login
```http
POST /auth/login
Content-Type: multipart/form-data

username=seu@email.com&password=suasenha
```

#### Refresh Token
```http
POST /auth/refresh
Content-Type: application/json

{
  "refresh_token": "eyJhbGc..."
}
```

#### Get Current User
```http
GET /auth/me
Authorization: Bearer {token}
```

---

### 📁 Projects

#### List Projects
```http
GET /projects
Authorization: Bearer {token}
```

**Response:**
```json
[
  {
    "id": 1,
    "name": "Projeto Exemplo",
    "description": "Descrição do projeto",
    "status": "active",
    "start_date": "2024-01-01T00:00:00Z",
    "end_date": null,
    "created_at": "2024-01-01T00:00:00Z",
    "updated_at": null
  }
]
```

#### Create Project (Admin only)
```http
POST /projects
Authorization: Bearer {token}
Content-Type: application/json

{
  "name": "Novo Projeto",
  "description": "Descrição",
  "status": "active",
  "start_date": "2024-01-01T00:00:00Z",
  "user_ids": [2, 3]
}
```

#### Get Project
```http
GET /projects/{project_id}
Authorization: Bearer {token}
```

#### Update Project (Admin only)
```http
PUT /projects/{project_id}
Authorization: Bearer {token}
Content-Type: application/json

{
  "name": "Projeto Atualizado",
  "status": "completed"
}
```

#### Delete Project (Admin only)
```http
DELETE /projects/{project_id}
Authorization: Bearer {token}
```

---

### 🎥 Recordings

#### List Recordings
```http
GET /recordings?project_id=1
Authorization: Bearer {token}
```

#### Upload Recording (Admin only)
```http
POST /recordings
Authorization: Bearer {token}
Content-Type: multipart/form-data

project_id=1
title=Aula 01
description=Introdução ao Python
file=@video.mp4
```

#### Get Recording
```http
GET /recordings/{recording_id}
Authorization: Bearer {token}
```

#### Get Download URL
```http
GET /recordings/{recording_id}/download-url
Authorization: Bearer {token}
```

**Response:**
```json
{
  "download_url": "https://sharepoint.com/download/..."
}
```

#### Update Recording (Admin only)
```http
PUT /recordings/{recording_id}
Authorization: Bearer {token}
Content-Type: application/json

{
  "title": "Aula 01 - Atualizada",
  "description": "Nova descrição"
}
```

#### Delete Recording (Admin only)
```http
DELETE /recordings/{recording_id}
Authorization: Bearer {token}
```

---

### 📅 Bookings

#### List Bookings
```http
GET /bookings
Authorization: Bearer {token}
```

#### List Available Slots
```http
GET /bookings/slots?available_only=true
Authorization: Bearer {token}
```

#### Create Availability Slot (Admin only)
```http
POST /bookings/slots
Authorization: Bearer {token}
Content-Type: application/json

{
  "start_time": "2024-01-15T14:00:00Z",
  "end_time": "2024-01-15T15:00:00Z"
}
```

#### Create Booking
```http
POST /bookings
Authorization: Bearer {token}
Content-Type: application/json

{
  "slot_id": 1,
  "title": "Consultoria Python",
  "description": "Dúvidas sobre Django"
}
```

#### Update Booking (Admin only)
```http
PUT /bookings/{booking_id}
Authorization: Bearer {token}
Content-Type: application/json

{
  "status": "completed"
}
```

#### Cancel Booking
```http
DELETE /bookings/{booking_id}
Authorization: Bearer {token}
```

---

### 📄 Files

#### List Files
```http
GET /files?project_id=1
Authorization: Bearer {token}
```

#### Upload File (Admin only)
```http
POST /files
Authorization: Bearer {token}
Content-Type: multipart/form-data

project_id=1
name=Documento.pdf
description=Especificação do projeto
file=@documento.pdf
```

#### Get File
```http
GET /files/{file_id}
Authorization: Bearer {token}
```

#### Get Download URL
```http
GET /files/{file_id}/download-url
Authorization: Bearer {token}
```

**Response:**
```json
{
  "download_url": "https://sharepoint.com/download/..."
}
```

#### Update File (Admin only)
```http
PUT /files/{file_id}
Authorization: Bearer {token}
Content-Type: application/json

{
  "name": "Documento Atualizado.pdf",
  "description": "Nova descrição"
}
```

#### Delete File (Admin only)
```http
DELETE /files/{file_id}
Authorization: Bearer {token}
```

---

### 💬 Requests

#### List Requests
```http
GET /requests?project_id=1
Authorization: Bearer {token}
```

#### Create Request
```http
POST /requests
Authorization: Bearer {token}
Content-Type: application/json

{
  "project_id": 1,
  "title": "Problema no Login",
  "description": "Não consigo fazer login no sistema",
  "type": "bug"
}
```

**Types**: `improvement`, `revision`, `bug`, `question`

#### Get Request
```http
GET /requests/{request_id}
Authorization: Bearer {token}
```

#### Update Request
```http
PUT /requests/{request_id}
Authorization: Bearer {token}
Content-Type: application/json

{
  "status": "in_progress"
}
```

**Statuses**: `open`, `in_progress`, `completed`, `cancelled`

#### Delete Request
```http
DELETE /requests/{request_id}
Authorization: Bearer {token}
```

#### Add Message to Request
```http
POST /requests/{request_id}/messages
Authorization: Bearer {token}
Content-Type: application/json

{
  "message": "Já tentei resetar a senha, mas não funcionou."
}
```

#### List Request Messages
```http
GET /requests/{request_id}/messages
Authorization: Bearer {token}
```

---

## Error Responses

### 400 Bad Request
```json
{
  "detail": "Invalid input data"
}
```

### 401 Unauthorized
```json
{
  "detail": "Could not validate credentials"
}
```

### 403 Forbidden
```json
{
  "detail": "Not enough permissions"
}
```

### 404 Not Found
```json
{
  "detail": "Resource not found"
}
```

### 500 Internal Server Error
```json
{
  "detail": "Internal server error"
}
```

---

## Rate Limiting

Atualmente não há rate limiting implementado. Em produção, considere adicionar:
- `slowapi` para rate limiting no FastAPI
- Nginx/Cloudflare para proteção DDoS

## CORS

Por padrão, a API aceita requisições de:
- `http://localhost:3000`
- `http://frontend:3000`

Configure `CORS_ORIGINS` no `.env` para adicionar mais origens.

## Webhooks (Future)

Planejado para versões futuras:
- Webhook ao criar novo projeto
- Webhook ao agendar aula
- Webhook ao criar solicitação

## SDKs (Future)

SDKs planejados:
- Python SDK
- JavaScript/TypeScript SDK
- Mobile SDK (React Native)

## Changelog

### v1.0.0 (2024-01-01)
- 🎉 Release inicial
- ✅ Autenticação JWT
- ✅ CRUD de projetos
- ✅ Upload de gravações
- ✅ Sistema de agendamento
- ✅ Gerenciamento de arquivos
- ✅ Sistema de solicitações
