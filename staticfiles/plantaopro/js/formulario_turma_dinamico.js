
document.addEventListener('DOMContentLoaded', function () {
    const inputBusca = document.getElementById('buscaPessoa');
    const tipoPessoa = document.getElementById('tipoPessoa');
    const disciplinaSelect = document.getElementById('disciplinaSelecionada');
    const campoDisciplina = document.getElementById('campoDisciplina');
    const sugestoes = document.createElement('ul');

    sugestoes.id = 'sugestoes';
    sugestoes.className = 'autocomplete-lista';
    Object.assign(sugestoes.style, {
        position: 'absolute',
        zIndex: 1000,
        background: 'white',
        listStyle: 'none',
        padding: '0',
        marginTop: '0',
        width: '100%',
        border: '1px solid #ccc',
        maxHeight: '200px',
        overflowY: 'auto'
    });
    inputBusca.parentNode.appendChild(sugestoes);

    tipoPessoa.addEventListener('change', () => {
        inputBusca.value = '';
        sugestoes.innerHTML = '';
        sugestoes.dataset.lista = '[]';

        const tipo = tipoPessoa.value;
        if (tipo === 'professor') {
            campoDisciplina.style.display = 'block';
            disciplinaSelect.disabled = false;
        } else {
            campoDisciplina.style.display = 'none';
            disciplinaSelect.disabled = true;
            disciplinaSelect.value = '';
        }
    });

    inputBusca.addEventListener('input', function () {
        const nome = this.value.trim();
        const tipo = tipoPessoa.value;

        if (nome.length < 2) {
            sugestoes.innerHTML = '';
            return;
        }

        fetch(`/autocomplete_pessoa/?nome=${encodeURIComponent(nome)}&tipo=${tipo}`)
            .then(res => res.json())
            .then(data => {
                sugestoes.innerHTML = '';
                sugestoes.dataset.lista = JSON.stringify(data.resultados || []);

                data.resultados.forEach(pessoa => {
                    const item = document.createElement('li');
                    item.textContent = pessoa.nome;
                    Object.assign(item.style, {
                        padding: '8px',
                        cursor: 'pointer'
                    });

                    item.addEventListener('click', () => {
                        inputBusca.value = pessoa.nome;
                        sugestoes.innerHTML = '';
                    });

                    sugestoes.appendChild(item);
                });
            });
    });

    document.addEventListener('click', function (e) {
        if (!sugestoes.contains(e.target) && e.target !== inputBusca) {
            sugestoes.innerHTML = '';
        }
    });

    const turma = {
        professor: null,
        disciplina_id: null,
        alunos: []
    };

    window.adicionarPessoa = function () {
        const nome = inputBusca.value.trim();
        const tipo = tipoPessoa.value;
        const lista = sugestoes.dataset.lista ? JSON.parse(sugestoes.dataset.lista) : [];
        const pessoa = lista.find(p => p.nome === nome);

        if (!pessoa) {
            alert("Selecione um nome da lista.");
            return;
        }

        if (tipo === 'professor') {
            const disciplinaId = disciplinaSelect.value;
            const disciplinaNome = disciplinaSelect.options[disciplinaSelect.selectedIndex]?.text || '';

            if (!disciplinaId) {
                alert("Selecione uma disciplina para o professor.");
                return;
            }

            turma.professor = {
                id: pessoa.id,
                nome: pessoa.nome,
                disciplinaId: disciplinaId,
                disciplinaNome: disciplinaNome
            };
            turma.disciplina_id = disciplinaId;
            document.getElementById('professor_id').value = pessoa.id;
        } else {
            if (!turma.alunos.some(aluno => aluno.id === pessoa.id)) {
                turma.alunos.push({ id: pessoa.id, nome: pessoa.nome });
            }
        }

        atualizarListaTurma();
        inputBusca.value = '';
        sugestoes.innerHTML = '';
    };

    function atualizarListaTurma() {
        const campo = document.getElementById('turmaMontada');
        const inputAlunosIds = document.getElementById('alunos_ids');
        let texto = '';

        if (turma.professor) {
        const disciplinaSelect = document.getElementById('disciplinaSelecionada');
        const disciplinaNome = disciplinaSelect.options[disciplinaSelect.selectedIndex]?.text || '';
        texto += `👨‍🏫 ${turma.professor.nome}${disciplinaNome ? ' – ' + disciplinaNome : ''}\n`;
}

        if (turma.alunos.length) {
            const alunosOrdenados = turma.alunos
                .map(a => ({ ...a }))
                .sort((a, b) => a.nome.localeCompare(b.nome));

            alunosOrdenados.forEach(a => {
                texto += `👦 ${a.nome}\n`;
            });

            inputAlunosIds.value = alunosOrdenados.map(a => a.id).join(',');
        } else {
            inputAlunosIds.value = '';
        }

        campo.value = texto.trim();
    }

    document.getElementById('turmaForm').addEventListener('submit', function (e) {
        e.preventDefault();

        const nome = document.getElementById('nomeTurma').value.trim();
        const turno = document.getElementById('turnoTurma').value.trim();
        const ano = document.getElementById('anoTurma').value.trim();
        const sala = document.getElementById('salaTurma').value.trim();
        const descricao = document.getElementById('descricaoTurma').value.trim();

        const professorId = document.getElementById('professor_id').value.trim();
        const disciplinaId = document.getElementById('disciplinaSelecionada').value.trim();
        const alunosIdsStr = document.getElementById('alunos_ids').value.trim();
        const alunosIds = alunosIdsStr ? alunosIdsStr.split(',') : [];

        if (!nome || !turno || !ano || !sala) {
            alert("Preencha todos os campos obrigatórios.");
            return;
        }
        if (!professorId) {
            alert("Adicione um professor à turma.");
            return;
        }
        if (!disciplinaId) {
            alert("Associe uma disciplina ao professor.");
            return;
        }
        if (!alunosIds.length) {
            alert("Adicione pelo menos um aluno à turma.");
            return;
        }

        fetch('/criar_turma/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': getCookie('csrftoken')
            },
            body: JSON.stringify({
                nome,
                turno,
                ano,
                sala,
                descricao,
                professor_id: professorId,
                disciplina_id: disciplinaId,
                alunos_ids: alunosIds
            })
        })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                alert(data.mensagem);
                window.location.reload();
            } else {
                alert("Erro: " + data.mensagem);
            }
        })
        .catch(error => {
            console.error('Erro ao salvar turma:', error);
            alert("Erro inesperado ao salvar turma.");
        });
    });

    function getCookie(name) {
        let cookieValue = null;
        if (document.cookie && document.cookie !== '') {
            const cookies = document.cookie.split(';');
            for (let cookie of cookies) {
                cookie = cookie.trim();
                if (cookie.startsWith(name + '=')) {
                    cookieValue = decodeURIComponent(cookie.slice(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }

    atualizarCampoDisciplina();
});
