// Função para efetuar login e obter o token JWT
function login(event) {
    event.preventDefault();
    const username = document.getElementById('username').value;
    const password = document.getElementById('password').value;

    fetch('/login', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ username, password })
    })
    .then(response => {
        if (!response.ok) {
            throw new Error('Falha no login');
        }
        return response.json();
    })
    .then(data => {
        localStorage.setItem('jwtToken', data.access_token);
        // Após o login bem-sucedido, buscar tarefas
        buscarTarefas();
    })
    .catch(error => {
        console.error('Erro ao fazer login:', error);
        alert('Usuário ou senha incorretos.');
    });
}

// Função para buscar e renderizar as tarefas da API
function buscarTarefas() {
    const jwtToken = localStorage.getItem('jwtToken');
    if (!jwtToken) {
        // Se não há token, exibir o formulário de login
        document.getElementById('login-form').style.display = 'block';
        document.getElementById('app-content').style.display = 'none';
        return;
    }

    document.getElementById('login-form').style.display = 'none';
    document.getElementById('app-content').style.display = 'block';

    fetch('/tasks', {
        headers: { 'Authorization': 'Bearer ' + jwtToken }
    })
    .then(response => {
        if (response.status === 401) {
            // Token inválido ou expirado
            localStorage.removeItem('jwtToken');
            buscarTarefas();
            throw new Error('Não autorizado');
        }
        return response.json();
    })
    .then(tarefas => {
        // Armazenar tarefas em uma variável global para pesquisa e filtro
        window.tarefasGlobais = tarefas;
        renderizarTarefas(tarefas);
    })
    .catch(error => console.error('Erro ao buscar tarefas:', error));
}

// Função para renderizar tarefas
function renderizarTarefas(tarefas) {
    const listaTarefas = document.getElementById('lista-tarefas');
    listaTarefas.innerHTML = '';  // Limpa a lista de tarefas

    tarefas.forEach(tarefa => {
        const li = document.createElement('li');
        li.classList.toggle('completed', tarefa.status === 'complete');
        li.innerHTML = `
            <span>${tarefa.title}</span>
            ${tarefa.status === 'complete' ? 
            `<div class="check" onclick="confirmarExclusao(${tarefa.id})">
                <i class="fa-solid fa-trash"></i>
            </div>` :
            `<div class="hamburger-menu">
                <i class="fa-solid fa-bars"></i>
                <div class="menu-options">
                    <button onclick="concluirTarefa(${tarefa.id})">
                        <i class="fa-solid fa-check"></i>
                    </button>
                    <button onclick="editarTarefa(${tarefa.id}, '${tarefa.title.replace(/'/g, "\\'")}')">
                        <i class="fa-solid fa-edit"></i>
                    </button>
                    <button onclick="confirmarExclusao(${tarefa.id})">
                        <i class="fa-solid fa-trash"></i>
                    </button>
                </div>
            </div>`}
        `;
        listaTarefas.appendChild(li);
    });
}

// Função para adicionar uma nova tarefa
function adicionarTarefa(event) {
    event.preventDefault();
    const titulo = document.getElementById('titulo-tarefa').value;
    const jwtToken = localStorage.getItem('jwtToken');

    fetch('/tasks', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'Authorization': 'Bearer ' + jwtToken
        },
        body: JSON.stringify({ title: titulo })
    })
    .then(response => {
        if (response.status === 401) {
            localStorage.removeItem('jwtToken');
            buscarTarefas();
            throw new Error('Não autorizado');
        }
        return response.json();
    })
    .then(() => {
        buscarTarefas();
        document.getElementById('titulo-tarefa').value = '';
    })
    .catch(error => console.error('Erro ao adicionar tarefa:', error));
}

// Função para concluir tarefa
function concluirTarefa(id) {
    const jwtToken = localStorage.getItem('jwtToken');

    fetch(`/tasks/${id}`, {
        method: 'PUT',
        headers: { 
            'Content-Type': 'application/json', 
            'Authorization': 'Bearer ' + jwtToken 
        },
        body: JSON.stringify({ status: 'complete' })
    })
    .then(response => {
        if (response.status === 401) {
            localStorage.removeItem('jwtToken');
            buscarTarefas();
            throw new Error('Não autorizado');
        }
        buscarTarefas();
    })
    .catch(error => console.error('Erro ao concluir tarefa:', error));
}

// Função para editar tarefa
function editarTarefa(id, tituloAtual) {
    const novoTitulo = prompt('Editar tarefa:', tituloAtual);
    if (novoTitulo !== null && novoTitulo.trim() !== '') {
        const jwtToken = localStorage.getItem('jwtToken');

        fetch(`/tasks/${id}`, {
            method: 'PUT',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': 'Bearer ' + jwtToken
            },
            body: JSON.stringify({ title: novoTitulo })
        })
        .then(response => {
            if (response.status === 401) {
                localStorage.removeItem('jwtToken');
                buscarTarefas();
                throw new Error('Não autorizado');
            }
            buscarTarefas();
        })
        .catch(error => console.error('Erro ao editar tarefa:', error));
    }
}

// Função para confirmar exclusão
function confirmarExclusao(id) {
    const confirmar = confirm('Tem certeza que deseja excluir esta tarefa?');
    if (confirmar) {
        excluirTarefa(id);
    }
}

// Função para excluir tarefa
function excluirTarefa(id) {
    const jwtToken = localStorage.getItem('jwtToken');

    fetch(`/tasks/${id}`, {
        method: 'DELETE',
        headers: { 'Authorization': 'Bearer ' + jwtToken }
    })
    .then(response => {
        if (response.status === 401) {
            localStorage.removeItem('jwtToken');
            buscarTarefas();
            throw new Error('Não autorizado');
        }
        buscarTarefas();
    })
    .catch(error => console.error('Erro ao excluir tarefa:', error));
}

// Funções de pesquisa e filtro
function pesquisarTarefas() {
    const termoPesquisa = document.getElementById('search-bar').value.toLowerCase();
    const tarefas = window.tarefasGlobais || [];
    const tarefasFiltradas = tarefas.filter(t => t.title.toLowerCase().includes(termoPesquisa));
    renderizarTarefas(tarefasFiltradas);
}

function filtrarTarefas(filtro) {
    const tarefas = window.tarefasGlobais || [];
    let tarefasFiltradas = tarefas;
    if (filtro === 'pendentes') tarefasFiltradas = tarefas.filter(t => t.status === 'pending');
    else if (filtro === 'concluidas') tarefasFiltradas = tarefas.filter(t => t.status === 'complete');
    renderizarTarefas(tarefasFiltradas);
}

// Função para alternar tema
function alternarTema() {
    document.body.classList.toggle('dark');
    const temaIcon = document.getElementById('tema-toggle');
    temaIcon.textContent = document.body.classList.contains('dark') ? '🌞' : '🌙';
}

// Carregar as tarefas ao carregar a página
window.onload = buscarTarefas;

// Adicionar event listener para o formulário de login
document.querySelector('#login-form form').addEventListener('submit', login);

// Adicionar event listener para o formulário de nova tarefa
document.getElementById('form-tarefa').addEventListener('submit', adicionarTarefa);
