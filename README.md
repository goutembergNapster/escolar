# 🏫 Sistema Escolar - Escolinha

Este projeto é um sistema escolar completo desenvolvido com Django, que permite o gerenciamento de escolas, alunos, professores, turmas, disciplinas, boletins e mais.

## 🚀 Funcionalidades

- Cadastro e edição de escolas
- Cadastro de alunos, professores e funcionários
- Associação de alunos e professores a turmas
- Lançamento de notas por disciplina e bimestre
- Geração de boletins individuais
- Filtros de busca e status (ativo/inativo)
- Interface moderna e responsiva

## 🛠️ Tecnologias utilizadas

- Python 3.11
- Django 4.x
- HTML, CSS, JavaScript
- Bootstrap
- PostgreSQL
- Docker (opcional)
- Render (deploy)

## 📦 Instalação local

1. Clone o repositório:
   ```bash
   git clone https://github.com/seu-usuario/seu-projeto-escolinha.git
   cd seu-projeto-escolinha

Crie um ambiente virtual e ative:

python -m venv venv
source venv/bin/activate  # ou venv\Scripts\activate no Windows
Instale as dependências:

pip install -r requirements.txt
Rode as migrações e inicie o servidor:

python manage.py migrate
python manage.py runserver
👤 Acesso inicial
Você pode criar um superusuário para acessar o admin:

python manage.py createsuperuser
📁 Organização
home/ – App principal com models de Escola, Aluno, Docente etc.

templates/ – Páginas HTML com identidade visual personalizada

static/ – Estilos, scripts e imagens do sistema


📌 Licença
Este projeto é de uso privado e educativo, não sendo licenciado para uso comercial sem autorização.