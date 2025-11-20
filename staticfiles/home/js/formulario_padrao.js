document.addEventListener('DOMContentLoaded', () => {
    const submitButton = document.getElementById("submitButton");
    const buscarBtn = document.querySelector("[onclick^='buscarCpf'], [onclick^='buscarCnpj']");
    const cpfInput = document.getElementById("cpf") || document.getElementById("doctorCpf") || document.getElementById("cnpj");

    // Habilita todos os campos de input quando a página carrega
    enableFields();

    // Habilita o botão de submit
    if (submitButton) submitButton.disabled = false;

    // Atribui função de busca se botão existir
    if (buscarBtn && cpfInput) {
        buscarBtn.addEventListener('click', () => {
            const valor = cpfInput.value;
            if (!valor || valor.length < 11) {
                alert("Por favor, informe um CPF ou CNPJ válido.");
                return;
            }

            const rota = buscarBtn.getAttribute('onclick').includes('Cpf') ? '/buscar_cpf/' : '/buscar_cnpj/';
            const campoChave = rota.includes('cpf') ? 'cpf' : 'cnpj';

            fetch(rota, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': getCsrfToken()
                },
                body: JSON.stringify({ [campoChave]: valor })
            })
            .then(res => res.json())
            .then(data => {
                if (data.exists) {
                    preencherCampos(data.dados || data.professor || data.funcionario || data.escola);
                    enableFields();
                } else {
                    alert('Não encontrado. Preencha os campos.');
                    limparCampos();
                    enableFields();
                }
            })
            .catch(error => console.error("Erro:", error));
        });
    }
});

function enableFields() {
    document.querySelectorAll('input, select, textarea').forEach(el => {
        el.disabled = false;
        el.style.backgroundColor = "white";
    });
}

function preencherCampos(data) {
    for (let key in data) {
        const el = document.getElementById(key);
        if (el) el.value = data[key];
    }
}

function limparCampos() {
    document.querySelectorAll('input, select, textarea').forEach(el => {
        if (el.type !== "hidden") el.value = "";
    });
}

function getCsrfToken() {
    const cookieValue = document.cookie
        .split('; ')
        .find(row => row.startsWith('csrftoken='));
    return cookieValue ? cookieValue.split('=')[1] : '';
}
