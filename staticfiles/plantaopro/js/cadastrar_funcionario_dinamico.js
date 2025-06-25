document.addEventListener("DOMContentLoaded", function () {
    const form = document.getElementById("funcionarioForm");
    const submitButton = document.getElementById("submitButton");

    form.addEventListener("input", () => {
        const cpf = form.cpf.value.trim();
        const nome = form.nome.value.trim();
        const email = form.email.value.trim();
        const telefone = form.telefone.value.trim();
        const cargo = form.cargo.value.trim();
        submitButton.disabled = !(cpf && nome && email && telefone && cargo);
    });

    form.addEventListener("submit", function (e) {
        e.preventDefault();

        const data = {
            cpf: form.cpf.value,
            nome: form.nome.value,
            rg: form.rg.value,
            sexo: form.sexo.value,
            data_nascimento: form.nascimento.value,
            estado_civil: form.estado_civil.value,
            escolaridade: form.escolaridade.value,
            turno_trabalho: form.turno.value,
            carga_horaria: form.carga_horaria.value,
            tipo_vinculo: form.vinculo.value,
            observacoes: form.observacoes.value,
            cep: form.cep.value,
            endereco: form.address.value,
            numero: form.numero?.value || '',
            complemento: form.complemento?.value || '',
            bairro: form.bairro.value,
            cidade: form.city.value,
            estado: form.state.value,
            telefone: form.telefone.value,
            email: form.email.value,
            cargo: form.cargo.value,  // agora vem do input do usuário
            ativo: true
        };

        fetch("/cadastrar-funcionario/", {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
                "X-CSRFToken": document.querySelector('[name=csrfmiddlewaretoken]').value,
            },
            body: JSON.stringify(data),
        })
        .then(res => res.json())
        .then(response => {
            if (response.success) {
                alert("Funcionário cadastrado com sucesso!");
                form.reset();
                submitButton.disabled = true;
            } else {
                alert("Erro: " + (response.error || "Falha no cadastro."));
            }
        })
        .catch(err => {
            console.error("Erro ao cadastrar funcionário:", err);
            alert("Erro inesperado ao cadastrar funcionário.");
        });
    });
});