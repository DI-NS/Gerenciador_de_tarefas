from flask import Flask, request, jsonify, render_template
from flask_jwt_extended import JWTManager, create_access_token, jwt_required
import mysql.connector
import redis
import json
import html  # Para sanitizar as entradas de usuário
import os
import logging

# Configurações de JWT e Redis
JWT_SECRET_KEY = os.getenv('JWT_SECRET_KEY', 'sua_chave_secreta_jwt')
REDIS_HOST = os.getenv('REDIS_HOST')
REDIS_PORT = int(os.getenv('REDIS_PORT', 6379))
REDIS_DB = int(os.getenv('REDIS_DB', 0))

# Verificar se as variáveis essenciais estão definidas
if not all([JWT_SECRET_KEY, REDIS_HOST]):
    raise EnvironmentError("Variáveis de ambiente essenciais não estão definidas.")

# Inicializar o Flask
app = Flask(__name__)
app.config['JWT_SECRET_KEY'] = JWT_SECRET_KEY

# Configurar JWT
jwt = JWTManager(app)

# Configurar logging
logging.basicConfig(level=logging.INFO)

# Função para sanitizar entradas
def sanitize_input(input_str):
    """Sanitiza a entrada do usuário para evitar injeção de código."""
    return html.escape(input_str)

# Simulação de banco de usuários
users = {"admin": "senha123"}  # Para testes futuros, tenho que substituir por um banco de dados

# Função para obter a conexão com o MySQL
def get_db_connection():
    """Estabelece uma conexão com o banco de dados MySQL."""
    MYSQL_USER = os.getenv('MYSQL_USER', 'root')
    MYSQL_PASSWORD = os.getenv('MYSQL_PASSWORD')
    MYSQL_DB = os.getenv('MYSQL_DB', 'gerenciador_tarefas')
    INSTANCE_CONNECTION_NAME = os.getenv('INSTANCE_CONNECTION_NAME')  # Nome de conexão do Cloud SQL

    if os.getenv('GAE_ENV', '').startswith('standard'):
        # Conexão quando rodando no App Engine
        try:
            conn = mysql.connector.connect(
                user=MYSQL_USER,
                password=MYSQL_PASSWORD,
                unix_socket='/cloudsql/{}'.format(INSTANCE_CONNECTION_NAME),
                database=MYSQL_DB
            )
            return conn
        except mysql.connector.Error as err:
            app.logger.error(f"Erro ao conectar ao MySQL: {err}")
            raise
    else:
        # Conexão local para testes
        MYSQL_HOST = os.getenv('MYSQL_HOST', 'localhost')
        try:
            conn = mysql.connector.connect(
                host=MYSQL_HOST,
                user=MYSQL_USER,
                password=MYSQL_PASSWORD,
                database=MYSQL_DB
            )
            return conn
        except mysql.connector.Error as err:
            app.logger.error(f"Erro ao conectar ao MySQL: {err}")
            raise

@app.route('/')
def index():
    """Renderiza a página principal."""
    return render_template('index.html')

@app.route('/login', methods=['POST'])
def login():
    """Efetua login e retorna o token JWT."""
    username = request.json.get('username', None)
    password = request.json.get('password', None)
    
    if username not in users or users[username] != password:
        return jsonify({"msg": "Usuário ou senha incorretos"}), 401

    access_token = create_access_token(identity=username)
    return jsonify(access_token=access_token)

@app.route('/tasks', methods=['GET'])
@jwt_required()
def get_tasks():
    """Lista todas as tarefas, usando Redis como cache."""
    try:
        r = redis.Redis(host=REDIS_HOST, port=REDIS_PORT, db=REDIS_DB)
        cached_tasks = r.get('tasks')
        if cached_tasks:
            return jsonify(json.loads(cached_tasks)), 200
    except redis.ConnectionError as e:
        app.logger.error(f"Erro ao conectar ao Redis: {e}")

    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute('SELECT * FROM tasks')
    tasks = cursor.fetchall()
    
    cursor.close()
    conn.close()

    try:
        r.setex('tasks', 60, json.dumps(tasks))  # Cache com expiração de 60 segundos
    except redis.ConnectionError as e:
        app.logger.error(f"Erro ao conectar ao Redis ao definir cache: {e}")

    return jsonify(tasks), 200

@app.route('/tasks', methods=['POST'])
@jwt_required()
def add_task():
    """Adiciona uma nova tarefa."""
    data = request.get_json()
    title = sanitize_input(data.get('title', '').strip())
    
    if not title:
        return jsonify({"error": "O título da tarefa não pode estar vazio"}), 400

    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute('INSERT INTO tasks (title) VALUES (%s)', (title,))
    conn.commit()

    new_task_id = cursor.lastrowid
    cursor.execute('SELECT * FROM tasks WHERE id = %s', (new_task_id,))
    new_task = cursor.fetchone()

    cursor.close()
    conn.close()

    try:
        r = redis.Redis(host=REDIS_HOST, port=REDIS_PORT, db=REDIS_DB)
        r.delete('tasks')  # Limpa cache de tarefas após inserção
    except redis.ConnectionError as e:
        app.logger.error(f"Erro ao conectar ao Redis ao deletar cache: {e}")

    return jsonify(new_task), 201

@app.route('/tasks/<int:task_id>', methods=['PUT'])
@jwt_required()
def update_task(task_id):
    """Atualiza o status ou título de uma tarefa."""
    data = request.get_json()
    status = data.get('status')
    title = data.get('title')

    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    if status and title:
        status = sanitize_input(status)
        title = sanitize_input(title)
        cursor.execute('UPDATE tasks SET status = %s, title = %s WHERE id = %s', (status, title, task_id))
    elif status:
        status = sanitize_input(status)
        cursor.execute('UPDATE tasks SET status = %s WHERE id = %s', (status, task_id))
    elif title:
        title = sanitize_input(title)
        cursor.execute('UPDATE tasks SET title = %s WHERE id = %s', (title, task_id))
    else:
        return jsonify({'error': 'Nenhum dado para atualizar'}), 400

    conn.commit()

    cursor.execute('SELECT * FROM tasks WHERE id = %s', (task_id,))
    updated_task = cursor.fetchone()

    cursor.close()
    conn.close()

    if updated_task:
        try:
            r = redis.Redis(host=REDIS_HOST, port=REDIS_PORT, db=REDIS_DB)
            r.delete('tasks')  # Limpa cache após atualização
        except redis.ConnectionError as e:
            app.logger.error(f"Erro ao conectar ao Redis ao deletar cache: {e}")
        return jsonify(updated_task), 200
    return jsonify({'error': 'Tarefa não encontrada'}), 404

@app.route('/tasks/<int:task_id>', methods=['DELETE'])
@jwt_required()
def delete_task(task_id):
    """Remove uma tarefa."""
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('DELETE FROM tasks WHERE id = %s', (task_id,))
    conn.commit()

    cursor.close()
    conn.close()

    if cursor.rowcount > 0:
        try:
            r = redis.Redis(host=REDIS_HOST, port=REDIS_PORT, db=REDIS_DB)
            r.delete('tasks')  # Limpa cache após remoção
        except redis.ConnectionError as e:
            app.logger.error(f"Erro ao conectar ao Redis ao deletar cache: {e}")
        return '', 204
    return jsonify({'error': 'Tarefa não encontrada'}), 404

# Rodar o servidor Flask
if __name__ == '__main__':
    app.run(debug=True)
