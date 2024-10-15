# Gerenciador de Tarefas

**URL da Aplicação:** [Gerenciador de Tarefas](https://gerenciador-tarefas-438612.uc.r.appspot.com)

## Sumário

- [Descrição do Projeto](#descrição-do-projeto)
- [Funcionalidades](#funcionalidades)
- [Demonstração](#demonstração)
- [Tecnologias Utilizadas](#tecnologias-utilizadas)
- [Arquitetura do Projeto](#arquitetura-do-projeto)
- [Instalação e Configuração](#instalação-e-configuração)
- [Endpoints da API](#endpoints-da-api)
- [Deploy na Google Cloud Platform](#deploy-na-google-cloud-platform)
- [Considerações de Segurança](#considerações-de-segurança)
- [Contribuição](#contribuição)
- [Licença](#licença)
- [Contato](#contato)

## Descrição do Projeto

O **Gerenciador de Tarefas** é uma aplicação web desenvolvida para auxiliar usuários na organização e gerenciamento de suas tarefas diárias. A aplicação permite criar, visualizar, atualizar e deletar tarefas de maneira simples e intuitiva, além de oferecer funcionalidades de filtragem e pesquisa.

## Funcionalidades

- **Adicionar Tarefas:** Permite ao usuário criar novas tarefas com um título.
- **Listar Tarefas:** Exibe todas as tarefas cadastradas.
- **Atualizar Tarefas:** Possibilita marcar tarefas como concluídas.
- **Excluir Tarefas:** Remove tarefas indesejadas.
- **Filtrar Tarefas:** Filtra tarefas por status (todas, pendentes, concluídas).
- **Pesquisar Tarefas:** Pesquisa tarefas por palavras-chave.
- **Alternar Tema:** Alterna entre modos claro e escuro para melhor usabilidade.

## Demonstração

A aplicação está hospedada e pode ser acessada através do seguinte link:

- [Gerenciador de Tarefas](https://gerenciador-tarefas-438612.uc.r.appspot.com)

## Tecnologias Utilizadas

### Frontend

- **HTML5:** Estruturação do conteúdo da página.
- **CSS3:** Estilização e responsividade.
- **JavaScript (ES6+):** Manipulação dinâmica da página.
- **Font Awesome:** Ícones para melhorar a interface.

### Backend

- **Python 3:** Linguagem de programação para o backend.
- **Flask:** Microframework web para Python.
- **Flask-JWT-Extended:** Gerenciamento de autenticação JWT.
- **MySQL:** Banco de dados relacional para armazenamento das tarefas.
- **Redis:** Sistema de cache para melhorar a performance.
- **Gunicorn:** Servidor WSGI para aplicações Python.

### Outros

- **Google Cloud Platform (GCP):** Hospedagem da aplicação.

## Arquitetura do Projeto

O frontend é composto por um arquivo HTML para a interface, com um arquivo CSS para a estilização e um arquivo JavaScript para as interações dinâmicas:

- `templates/index.html`: Estrutura da página com barra de pesquisa, filtro e exibição das tarefas.
- `static/style.css`: Estilos para a página, com suporte a temas claro e escuro.
- `static/script.js`: Lógica do frontend, responsável por buscar tarefas da API, manipular os dados e gerenciar as interações com o usuário.

O backend é construído com Flask e está organizado da seguinte maneira:

- **`app.py`:** Arquivo principal da aplicação Flask, contendo as rotas e lógica de negócio.
- **Banco de Dados:** MySQL para armazenamento das tarefas.
- **Cache:** Redis para cache das tarefas e melhoria de performance.

### Descrição dos Arquivos

#### `templates/index.html`

- Estrutura a interface do usuário, incluindo:
  - Barra de pesquisa e filtros.
  - Formulário para adicionar novas tarefas.
  - Lista dinâmica de tarefas.
  - Modal para confirmação de exclusão.
  - Botão para alternar o tema da aplicação.

#### `static/style.css`

- Define estilos para:
  - Layout responsivo.
  - Temas claro e escuro.
  - Componentes como botões, menus e modais.
  - Animações e transições para melhor UX.

#### `static/script.js`

- Gerencia as interações do usuário com a interface:
  - Requisições à API usando `fetch`.
  - Manipulação do DOM para atualizar a lista de tarefas.
  - Funções para adicionar, atualizar, excluir e filtrar tarefas.
  - Implementação do tema claro/escuro.

#### `app.py`

- Configura a aplicação Flask:
  - Inicializa o app e configura o JWT.
  - Define rotas para CRUD das tarefas (`/tasks`).
  - Implementa autenticação JWT nas rotas protegidas.
  - Conexão com o banco de dados MySQL.
  - Utiliza Redis para cachear as tarefas.

## Instalação e Configuração

### Pré-requisitos

- **Python 3.x**
- **MySQL**
- **Redis**
- **Virtualenv** (opcional, mas recomendado)

### Passos para Configuração Local

1. **Clone o repositório:**

   ```bash
   git clone https://github.com/DI-NS/Gerenciador_de_tarefas
   ```

2. **Navegue até o diretório do projeto:**

   ```bash
   cd Gerenciador-de-tarefa
   ```

3. **Configuração do Ambiente Virtual (opcional):**

   ```bash
   python3 -m venv venv
   source venv/bin/activate  # Linux/Mac
   venv\Scripts\activate  # Windows
   ```

4. **Instale as dependências do backend:**

   ```bash
   pip install -r requirements.txt
   ```

5. **Configuração do Banco de Dados MySQL:**

   - Crie o banco de dados:

     ```sql
     CREATE DATABASE gerenciador_tarefas;
     ```

   - Crie a tabela:

     ```sql
     USE gerenciador_tarefas;
     CREATE TABLE tasks (
       id INT AUTO_INCREMENT PRIMARY KEY,
       title VARCHAR(255) NOT NULL,
       status VARCHAR(50) DEFAULT 'pending'
     );
     ```

6. **Configuração do Redis:**

   - Certifique-se de que o Redis está instalado e em execução na porta padrão (6379).

7. **Configure as Variáveis de Ambiente:**

   Configure as variáveis de ambiente para o JWT, Redis e MySQL:

   - `JWT_SECRET_KEY`
   - `REDIS_HOST` e `REDIS_PORT`
   - `MYSQL_USER`, `MYSQL_PASSWORD`, `MYSQL_HOST`, `MYSQL_DATABASE`

   Crie um arquivo `.env` na raiz do projeto e defina as seguintes variáveis:

   ```bash
   JWT_SECRET_KEY=your_jwt_secret_key
   REDIS_HOST=localhost
   REDIS_PORT=6379
   REDIS_DB=0
   MYSQL_HOST=localhost
   MYSQL_USER=your_mysql_user
   MYSQL_PASSWORD=your_mysql_password
   MYSQL_DATABASE=gerenciador_tarefas
   ```

8. **Inicie a Aplicação Flask:**

   ```bash
   python app.py
   ```

9. **Acesse a Aplicação:**

   Abra o navegador e visite `http://localhost:5000`

## Endpoints da API

| Método | Endpoint      | Descrição                     |
|--------|---------------|-------------------------------|
| GET    | `/tasks`      | Lista todas as tarefas        |
| POST   | `/tasks`      | Cria uma nova tarefa          |
| PUT    | `/tasks/<id>` | Atualiza uma tarefa existente |
| DELETE | `/tasks/<id>` | Remove uma tarefa             |

## Deploy na Google Cloud Platform

A aplicação está hospedada na Google Cloud Platform (GCP). A seguir estão os passos para realizar o deploy na GCP usando o Google App Engine.

### Pré-requisitos

- **Conta no Google Cloud Platform**
- **Google Cloud SDK instalado localmente**

### Passos para Deploy

1. **Crie um Projeto no GCP:**

   - Acesse o [Console do Google Cloud](https://console.cloud.google.com/).
   - Crie um novo projeto e anote o ID do projeto.

2. **Configure o Ambiente App Engine:**

   - Navegue até App Engine no console GCP e escolha a região desejada.

3. **Atualize o Arquivo `app.yaml`:**

   Crie um arquivo `app.yaml` na raiz do projeto com o seguinte conteúdo:

   ```yaml
   runtime: python39
   entrypoint: gunicorn -b :$PORT app:app

   handlers:
     - url: /static
       static_dir: static

     - url: /.*
       script: auto

   env_variables:
     JWT_SECRET_KEY: 'your_jwt_secret_key'
     MYSQL_HOST: 'your_mysql_host'
     MYSQL_USER: 'your_mysql_user'
     MYSQL_PASSWORD: 'your_mysql_password'
     MYSQL_DATABASE: 'gerenciador_tarefas'
     REDIS_HOST: 'your_redis_host'
     REDIS_PORT: '6379'
     REDIS_DB: '0'
   ```

   **Nota:** Certifique-se de substituir as variáveis de ambiente pelos valores corretos.

4. **Configure o Banco de Dados no GCP:**

   - **Cloud SQL:**
     - Crie uma instância MySQL no Cloud SQL.
     - Configure as permissões e anote o endereço público.
   - **Redis:**
     - Use o Memorystore para configurar uma instância Redis.

5. **Atualize as Regras de Firewall:**

   - Certifique-se de que as portas necessárias estão abertas para comunicação entre os serviços.

6. **Autentique-se no GCP:**

   ```bash
   gcloud auth login
   gcloud config set project your_project_id
   ```

7. **Instale Dependências de Produção:**

   Crie um arquivo `requirements.txt` com todas as dependências:

   ```bash
   Flask
   Flask-JWT-Extended
   mysql-connector-python
   redis
   gunicorn
   ```

8. **Realize o Deploy:**

   ```bash
   gcloud app deploy
   ```

   - Siga as instruções no terminal e aguarde a conclusão.

9. **Acesse a Aplicação:**

   - Após o deploy bem-sucedido, acesse a URL fornecida no terminal ou encontre-a no Console do GCP.

## Considerações de Segurança

- **Não Hardcode Senhas e Chaves:**
  - Evite colocar senhas e chaves secretas diretamente no código.
  - Use variáveis de ambiente ou serviços como o Secret Manager do GCP.
- **Configuração do JWT:**
  - Utilize chaves seguras e rotacione-as periodicamente.
- **Sanitização de Entradas:**
  - O código utiliza a função `html.escape` para evitar injeção de código.
- **Comunicação Segura:**
  - Considere usar HTTPS para comunicação segura entre o cliente e o servidor.
- **Gerenciamento de Dependências:**
  - Mantenha as dependências atualizadas para evitar vulnerabilidades conhecidas.

## Contato

- **Nome:** Diego Nunes Souza 
- **Email:** laynonjob@gmail.com
- **LinkedIn:** [Diego Nunes Souza](https://www.linkedin.com/in/diegodns/)
