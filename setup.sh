#!/bin/bash

echo "🚀 Blink Customers Platform - Setup Automático"
echo "=============================================="
echo ""

# Load .env if it exists
if [ -f .env ]; then
    export $(grep -v '^#' .env | xargs)
fi

# Check if .env exists
if [ ! -f .env ]; then
    echo "📝 Criando arquivo .env a partir do .env.example..."
    cp .env.example .env
    echo "✅ Arquivo .env criado!"
    echo "⚠️  IMPORTANTE: Edite o arquivo .env com suas credenciais antes de continuar em produção"
    echo ""
fi

# Start Docker Compose
echo "🐳 Iniciando containers Docker..."
docker-compose up -d

# Wait for database to be ready
echo "⏳ Aguardando banco de dados..."
sleep 5

# Create admin user
echo "👤 Criando usuário administrador..."
docker-compose exec -T backend python << 'EOF'
from app.database import SessionLocal
from app.models.user import User, UserRole
from app.utils.security import get_password_hash

db = SessionLocal()

# Check if admin already exists
import os
admin_email = os.getenv('ADMIN_EMAIL', 'admin@blinkpec.com')
admin_password = os.getenv('ADMIN_PASSWORD', 'changeme')
admin_name = os.getenv('ADMIN_NAME', 'Administrador')

existing_admin = db.query(User).filter(User.email == admin_email).first()

if existing_admin:
    print("⚠️  Admin já existe!")
else:
    admin = User(
        email=admin_email,
        hashed_password=get_password_hash(admin_password),
        full_name=admin_name,
        role=UserRole.ADMIN,
        is_active=True
    )
    db.add(admin)
    db.commit()
    print('✅ Admin criado com sucesso!')

db.close()
EOF

echo ""
echo "✅ Setup concluído!"
echo ""
echo "📌 Credenciais de Acesso:"
echo "   Email: $ADMIN_EMAIL (ou verifique o .env)"
echo "   Senha: $ADMIN_PASSWORD (ou verifique o .env)"
echo ""
echo "🌐 URLs:"
echo "   Frontend: http://localhost:3000"
echo "   Backend API: http://localhost:8000"
echo "   API Docs: http://localhost:8000/docs"
echo ""
echo "📖 Para mais informações, veja QUICKSTART.md"
echo ""
