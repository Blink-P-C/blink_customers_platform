# Contributing to Blink Customers Platform

Obrigado por considerar contribuir para o Blink Customers Platform! 🎉

## Como Contribuir

### 1. Reportar Bugs

Se você encontrou um bug, abra uma [issue](https://github.com/Blink-P-C/blink_customers_platform/issues) com:
- Descrição clara do problema
- Passos para reproduzir
- Comportamento esperado vs. atual
- Screenshots (se aplicável)
- Ambiente (OS, navegador, versão do Docker)

### 2. Sugerir Features

Para sugerir novas funcionalidades:
- Abra uma issue com a tag `enhancement`
- Descreva o caso de uso
- Explique como isso beneficiaria os usuários
- Se possível, sugira uma implementação

### 3. Pull Requests

#### Setup do Ambiente de Desenvolvimento

```bash
# Clone o repositório
git clone https://github.com/Blink-P-C/blink_customers_platform.git
cd blink_customers_platform

# Configure o ambiente
cp .env.example .env

# Inicie os serviços
docker-compose up -d

# Ou rode localmente:
# Backend
cd backend
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload

# Frontend (outro terminal)
cd frontend
npm install
npm run dev
```

#### Processo de Contribuição

1. **Fork** o repositório
2. **Crie uma branch** para sua feature:
   ```bash
   git checkout -b feature/minha-feature
   ```
3. **Faça suas alterações** seguindo os padrões do projeto
4. **Teste suas alterações**:
   - Backend: Execute os testes (quando disponíveis)
   - Frontend: Verifique no navegador
5. **Commit suas mudanças**:
   ```bash
   git commit -m "feat: adiciona nova funcionalidade X"
   ```
6. **Push para sua branch**:
   ```bash
   git push origin feature/minha-feature
   ```
7. **Abra um Pull Request** descrevendo suas mudanças

#### Padrões de Commit

Use [Conventional Commits](https://www.conventionalcommits.org/):

- `feat:` Nova funcionalidade
- `fix:` Correção de bug
- `docs:` Mudanças na documentação
- `style:` Formatação, ponto e vírgula, etc.
- `refactor:` Refatoração de código
- `test:` Adicionar ou modificar testes
- `chore:` Tarefas de manutenção

Exemplos:
```
feat: adiciona upload de múltiplos arquivos
fix: corrige erro ao deletar projeto
docs: atualiza README com novas instruções
```

### 4. Padrões de Código

#### Backend (Python/FastAPI)
- Siga [PEP 8](https://pep8.org/)
- Use type hints
- Docstrings para funções públicas
- Nomes de variáveis em `snake_case`
- Classes em `PascalCase`

```python
def create_project(
    project_data: ProjectCreate,
    db: Session = Depends(get_db)
) -> Project:
    """
    Create a new project.
    
    Args:
        project_data: Project data to create
        db: Database session
        
    Returns:
        Created project
    """
    pass
```

#### Frontend (TypeScript/React)
- Siga as [regras do ESLint](https://eslint.org/)
- Use componentes funcionais com hooks
- Props tipadas com TypeScript
- Nomes de componentes em `PascalCase`
- Funções/variáveis em `camelCase`

```typescript
interface ButtonProps {
  children: ReactNode
  variant?: 'primary' | 'secondary'
  onClick?: () => void
}

export default function Button({ children, variant = 'primary', onClick }: ButtonProps) {
  return (
    <button onClick={onClick} className={`btn btn-${variant}`}>
      {children}
    </button>
  )
}
```

### 5. Estrutura de Branches

- `main`: Código em produção
- `develop`: Desenvolvimento contínuo
- `feature/*`: Novas funcionalidades
- `fix/*`: Correções de bugs
- `hotfix/*`: Correções urgentes em produção

### 6. Revisão de Código

Todos os PRs passarão por revisão. Prepare-se para:
- Responder a comentários
- Fazer ajustes conforme sugerido
- Manter o código limpo e testável

### 7. Testes

Ao adicionar novas features:
- Adicione testes unitários (backend)
- Teste manualmente no navegador (frontend)
- Verifique se não quebrou funcionalidades existentes

### 8. Documentação

- Atualize o README se necessário
- Documente novas APIs no código
- Adicione exemplos de uso quando relevante

## Dúvidas?

Se tiver dúvidas sobre como contribuir, abra uma issue ou entre em contato:
- Email: contato@blinkpec.com
- GitHub Issues: https://github.com/Blink-P-C/blink_customers_platform/issues

## Código de Conduta

Seja respeitoso e profissional em todas as interações. Este é um projeto colaborativo e valorizamos a diversidade de ideias e experiências.

## Licença

Ao contribuir, você concorda que suas contribuições serão licenciadas sob a licença MIT do projeto.
