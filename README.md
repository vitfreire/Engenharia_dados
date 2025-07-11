# 🚀 Pipeline ETL – Servidores Públicos

Projeto prático de Engenharia de Dados.

---

## 🎯 Visão Geral

Este projeto realiza um pipeline completo de ETL (**Extração, Transformação e Carga**) com as seguintes etapas:

1. **Extração:** coleta dados do Portal da Transparência de Alagoas (API JSON).
2. **Carga:** salva os dados brutos em banco PostgreSQL.
3. **Transformação:** realiza limpeza e padronização usando DBT.
4. **Orquestração:** automatiza e gerencia o pipeline usando Prefect Cloud.

---

## 🧰 Tecnologias Utilizadas

| Camada        | Ferramenta                 | Descrição                            |
| ------------- | -------------------------- | ------------------------------------ |
| Orquestração  | **Prefect Cloud (v3)**     | Automação, monitoramento e deploy    |
| Transformação | **DBT**                    | Transformação SQL modular e testável |
| Armazenamento | **PostgreSQL**             | Armazena dados brutos e tratados     |
| Extração      | **Python 3.11 + Requests** | Consumo de API JSON                  |
| Tratamento    | **Pandas**                 | Manipulação e pré-processamento      |
| Conexão BD    | **SQLAlchemy**             | Comunicação Python com PostgreSQL    |
| Configuração  | **python-dotenv**          | Gerenciamento de variáveis sensíveis |

---

## 📂 Estrutura do Projeto

```
engenharia_dados/
├── etl/
│   ├── scrapping.py           # Extração e carga inicial
│   └── criar_banco.py         # Criação do banco e tabelas
├── flows/
│   └── flow_etl.py            # Definição do fluxo Prefect
├── dbt_project/
│   ├── models/
│   │   └── transformacoes/
│   │       ├── servidores.sql
│   │       └── servidores_tratados.sql
│   └── dbt_project.yml
├── prefect.yaml               # Configuração Prefect Cloud
├── requirements.txt           # Dependências do projeto
├── README.md
└── .gitignore
```

---

## ⚙️ Instalação e Configuração

### 1. Clone o repositório e configure o ambiente

```bash
git clone https://github.com/vitfreire/Engenharia_dados.git
cd <repo>

# Criar ambiente virtual
python -m venv .venv

# Ativar ambiente
# Windows
.venv\Scripts\activate
# Linux/macOS
source .venv/bin/activate

# Instalar dependências
pip install -r requirements.txt
```

### 2. Configuração das variáveis de ambiente

Crie um arquivo `.env` na raiz do projeto:

```env
DB_USER=<usuario>
DB_PASSWORD=<senha>
DB_HOST=localhost
DB_PORT=5432
DB_NAME=transparencia

API_ANO=2023
API_MES=7
API_LIMIT=200
API_OFFSET=0
```

Essas variáveis serão carregadas automaticamente pelo script com `load_dotenv()`.

### 3. Configuração DBT (fora do repositório)

Crie ou edite o arquivo `~/.dbt/profiles.yml`:

```yaml
transparencia:
  target: dev
  outputs:
    dev:
      type: postgres
      host: "{{ env_var('DB_HOST') }}"
      user: "{{ env_var('DB_USER') }}"
      password: "{{ env_var('DB_PASSWORD') }}"
      port: 5432
      dbname: "{{ env_var('DB_NAME') }}"
      schema: public
      threads: 1
```

---

## 🏃‍♀️ Execução Local

Execute os scripts na sequência abaixo:

```bash
python etl/criar_banco.py          # Cria banco e tabelas
python flows/flow_etl.py           # Executa o pipeline completo
```

---

## ☁️ Deploy com Prefect Cloud

### 1. Autenticação

```bash
prefect cloud login
```

### 2. Criação do Deployment

```bash
prefect deploy
```

### 3. Execução via interface web

No Prefect Cloud:

```
Flows → pipeline_etl → Deployments → pipeline_servidores_deploy → Run
```


## 📌 Autoria

**Vitória Freire**
Analista de Sistemas
[LinkedIn](https://www.linkedin.com/in/vitoriafreiredev)

---




