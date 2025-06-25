
document.addEventListener('DOMContentLoaded', () => {
    const inputBusca = document.getElementById('buscaPessoa');
    const selectTipo = document.getElementById('tipoPessoa');
    const turmaMontada = document.getElementById('turmaMontada');
    const turma = {
        professor: null,
        alunos: []
    };

    let resultadosBusca = [];

    inputBusca.addEventListener('input', async () => {
        const termo = inputBusca.value.trim();
        const tipo = selectTipo.value;
        if (termo.length < 2) return;

        try {
            const response = await fetch(`/buscar_${tipo}/?q=${encodeURIComponent(termo)}`);
            if (!response.ok) throw new Error('Erro na busca');
            resultadosBusca = await response.json();
            mostrarSugestoes(resultadosBusca);
        } catch (error) {
            console.error('Erro ao buscar:', error);
        }
    });

    window.adicionarPessoa = function () {
        const nome = inputBusca.value.trim();
        const tipo = selectTipo.value;

        if (!nome) return alert("Digite o nome da pessoa.");

        if (tipo === 'professor') {
            const professor = resultadosBusca.find(p => p.nome === nome);
            turma.professor = professor || { nome, disciplina: 'Disciplina não informada' };
        } else {
            if (!turma.alunos.some(a => a.nome === nome)) {
                const aluno = resultadosBusca.find(p => p.nome === nome) || { nome };
                turma.alunos.push(aluno);
            }
        }

        atualizarListaTurma();
        inputBusca.value = '';
        limparSugestoes();
    };

    function atualizarListaTurma() {
        let texto = '';
        if (turma.professor) {
            texto += `👨‍🏫 ${turma.professor.nome} – ${turma.professor.disciplina || 'Disciplina não informada'}\n`;
        }
        if (turma.alunos.length) {
            turma.alunos.sort((a, b) => a.nome.localeCompare(b.nome));
            turma.alunos.forEach(aluno => {
                texto += `👦 ${aluno.nome}\n`;
            });
        }
        turmaMontada.value = texto.trim();
    }

    function mostrarSugestoes(lista) {
        limparSugestoes();
        const datalist = document.createElement('datalist');
        datalist.id = 'sugestoesBusca';

        lista.forEach(pessoa => {
            const option = document.createElement('option');
            option.value = pessoa.nome;
            datalist.appendChild(option);
        });

        inputBusca.setAttribute('list', 'sugestoesBusca');
        document.body.appendChild(datalist);
    }

    function limparSugestoes() {
        const datalist = document.getElementById('sugestoesBusca');
        if (datalist) datalist.remove();
    }
});
