# 🚀 Quick Start Guide

## Setup Rápido (5 minutos)

### 1. Clone e configure
```bash
git clone https://github.com/Blink-P-C/blink_customers_platform.git
cd blink_customers_platform
cp .env.example .env
```

### 2. Inicie com Docker
```bash
docker-compose up -d
```

### 3. Crie o usuário admin
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
    role=UserRole.ADMIN,
    is_active=True
)
db.add(admin)
db.commit()
db.close()
print('✅ Admin criado com sucesso!')
print('Email: lincoln.oliver@blinkpec.com')
print('Senha: WEV7ui8YB3ay1v21')
"
```

### 4. Acesse a plataforma
- **Frontend**: http://localhost:3000
- **Login**: lincoln.oliver@blinkpec.com / WEV7ui8YB3ay1v21
- **API Docs**: http://localhost:8000/docs

### 5. Criar um cliente de teste
```bash
docker-compose exec backend python -c "
from app.database import SessionLocal
from app.models.user import User, UserRole
from app.utils.security import get_password_hash

db = SessionLocal()
client = User(
    email='cliente@exemplo.com',
    hashed_password=get_password_hash('cliente123'),
    full_name='Cliente Teste',
    role=UserRole.CLIENT,
    is_active=True
)
db.add(client)
db.commit()
db.close()
print('✅ Cliente criado com sucesso!')
print('Email: cliente@exemplo.com')
print('Senha: cliente123')
"
```

## ⚙️ Configuração de Integrações (Opcional)

### Microsoft SharePoint
1. Acesse [Azure Portal](https://portal.azure.com)
2. Crie um App Registration
3. Configure permissões: `Files.ReadWrite.All`, `Sites.ReadWrite.All`
4. Gere um client secret
5. Adicione ao `.env`:
   ```
   MICROSOFT_TENANT_ID=seu-tenant-id
   MICROSOFT_CLIENT_ID=seu-client-id
   MICROSOFT_CLIENT_SECRET=seu-client-secret
   SHAREPOINT_SITE_ID=seu-site-id
   SHAREPOINT_DRIVE_ID=seu-drive-id
   ```

### Google Calendar
1. Acesse [Google Cloud Console](https://console.cloud.google.com)
2. Crie um projeto e habilite a Google Calendar API
3. Crie credenciais OAuth 2.0
4. Adicione ao `.env`:
   ```
   GOOGLE_CLIENT_ID=seu-client-id
   GOOGLE_CLIENT_SECRET=seu-client-secret
   ```

## 📊 Fluxo de Uso

### Como Admin:
1. Login → Dashboard
2. Criar Projeto
3. Adicionar cliente ao projeto
4. Upload de gravações/arquivos
5. Definir slots de disponibilidade
6. Gerenciar solicitações

### Como Cliente:
1. Login → Dashboard
2. Ver seus projetos
3. Assistir gravações
4. Baixar arquivos
5. Agendar aulas
6. Criar solicitações

## 🔧 Comandos Úteis

```bash
# Ver logs
docker-compose logs -f

# Parar serviços
docker-compose down

# Rebuild completo
docker-compose down -v
docker-compose up --build

# Executar migrations
docker-compose exec backend alembic upgrade head

# Acessar banco de dados
docker-compose exec db psql -U postgres -d blink_customers

# Acessar shell do backend
docker-compose exec backend python

# Reinstalar dependências do frontend
docker-compose exec frontend npm install
```

## 🐛 Troubleshooting

### Porta já em uso
```bash
# Parar containers
docker-compose down

# Verificar portas
lsof -i :3000
lsof -i :8000
lsof -i :5432
```

### Banco de dados não inicia
```bash
# Remover volumes e recriar
docker-compose down -v
docker-compose up -d db
docker-compose logs db
```

### Frontend não carrega
```bash
# Rebuild do frontend
docker-compose up --build frontend
```

## 📝 Próximos Passos

1. ✅ Configure variáveis de ambiente em produção
2. ✅ Altere `SECRET_KEY` para uma chave forte e aleatória
3. ✅ Configure domínio e SSL (recomendado: Cloudflare + Vercel/Railway)
4. ✅ Configure backups automáticos do PostgreSQL
5. ✅ Implemente OAuth do Google Calendar (fluxo completo)
6. ✅ Personalize cores e branding no Tailwind config

## 🎯 Checklist de Produção

- [ ] Alterar todas as senhas padrão
- [ ] Configurar variáveis de ambiente seguras
- [ ] Habilitar HTTPS
- [ ] Configurar CORS adequadamente
- [ ] Implementar rate limiting
- [ ] Configurar monitoramento (Sentry, etc.)
- [ ] Fazer backup do banco de dados
- [ ] Testar integração SharePoint
- [ ] Testar integração Google Calendar
- [ ] Documentar processos internos
