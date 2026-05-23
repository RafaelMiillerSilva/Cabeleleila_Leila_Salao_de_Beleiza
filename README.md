# Cabeleleila Leila — Sistema de Agendamentos

Sistema de agendamento online desenvolvido com o framework **Django** para o salão Cabeleleila Leila.

O sistema esta disponivel em producao no Railway: https://cabeleleilaleilasalaodebeleiza-production.up.railway.app/
CONTA ADMIN PARA TESTE:
- Usuário: admin
- Email: admin@email.com
- Senha: admin123

---

## Sobre o Projeto

O sistema foi construído com regras de negócio personalizadas para atender às necessidades operacionais do salão:

- Alterações permitidas somente com antecedência mínima de **48 horas**
- Recomendação de **1 agendamento ativo por semana** por cliente
- Painel administrativo customizado no Django Admin
- Acompanhamento de faturamento e métricas gerenciais

---

## Como Executar o Projeto

O sistema pode ser iniciado de duas formas:

| Opção | Indicada para |
|---|---|
| [Docker (Recomendado)](#opcao-1--docker-recomendado) | Desenvolvimento rápido e isolado |
| [Execução Local](#opcao-2--execucao-local) | Ambientes sem Docker |

---

## Opcao 1 — Docker (Recomendado)

Esta opção provisiona automaticamente o servidor Django, o banco de dados PostgreSQL e um ambiente completamente isolado.

### Pré-requisitos

- Docker instalado
- Docker Compose instalado

### Passo a Passo

**1. Clone o repositório**

```bash
git clone https://github.com/RafaelMiillerSilva/Cabeleleila_Leila_Salao_de_Beleiza.git
cd Cabeleleila_Leila_Salao_de_Beleiza
```

**2. Suba os containers**

```bash
docker-compose up --build
```

**3. Execute as migrações**

Abra um novo terminal e rode:

```bash
docker-compose exec web python manage.py migrate
```

**4. Crie um superusuário**

```bash
docker-compose exec web python manage.py createsuperuser
```

**5. Acesse a aplicação**

| Serviço | URL |
|---|---|
| Sistema | http://localhost:8000 |
| Django Admin | http://localhost:8000/admin |

---

## Opcao 2 — Execucao Local

Nesta opção o Django roda diretamente no sistema operacional. Certifique-se de ter o **PostgreSQL instalado e em execução** com uma base de dados chamada `cabeleleila`.

### Pré-requisitos

- Python 3.13
- PostgreSQL instalado e rodando

### Passo a Passo

**1. Clone o repositório**

```bash
git clone https://github.com/RafaelMiillerSilva/Cabeleleila_Leila_Salao_de_Beleiza.git
cd Cabeleleila_Leila_Salao_de_Beleiza
```

**2. Crie e ative o ambiente virtual**

Windows:

```bash
python -m venv venv
.\venv\Scripts\activate
```

Linux / macOS:

```bash
python3 -m venv venv
source venv/bin/activate
```

**3. Instale as dependências**

```bash
pip install -r requirements.txt
```

**4. Configure as variáveis de ambiente**

Crie um arquivo `.env` na raiz do projeto com o seguinte conteúdo:

```env
DB_ENGINE=django.db.backends.postgresql
DB_NAME=cabeleleila
DB_USER=seu_usuario_postgres
DB_PASSWORD=sua_senha_postgres
DB_HOST=localhost
DB_PORT=5432
```

**5. Execute as migrações**

```bash
python manage.py migrate
```

**6. Crie um superusuário**

```bash
python manage.py createsuperuser
```

**7. Inicie o servidor**

```bash
python manage.py runserver
```

**8. Acesse a aplicação**

| Serviço | URL |
|---|---|
| Sistema | http://127.0.0.1:8000 |
| Django Admin | http://127.0.0.1:8000/admin |

---

## Tecnologias Utilizadas

| Tecnologia | Descrição |
|---|---|
| Django 2.1.2 | Framework web principal |
| PostgreSQL 15 | Banco de dados relacional |
| Docker | Containerização da aplicação |
| Docker Compose | Orquestração dos containers |
| Gunicorn | Servidor WSGI para produção |
| Railway | Plataforma de deploy em nuvem |

---

## Informacoes do Projeto

- **Framework:** Django 2.1.2
- **Banco de Dados:** PostgreSQL 15
- **Servidor de Produção:** Gunicorn
- **Deploy:** Preparado para Railway com estrutura Dockerizada