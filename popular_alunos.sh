#!/bin/bash

echo "Populando alunos para a escola ID 4..."

python3 manage.py shell <<EOF
from home.models import Aluno, Escola
from faker import Faker
from random import choice
from home.utils import gerar_matricula_unica
import random

fake = Faker('pt_BR')
escola = Escola.objects.get(id=3)

sexos = ['M', 'F']
tipos_sanguineos = ['A+', 'A-', 'B+', 'B-', 'O+', 'O-', 'AB+', 'AB-']

for i in range(30):
    nome = fake.name()
    sexo = choice(sexos)
    cpf = fake.cpf()
    aluno = Aluno.objects.create(
        nome=nome,
        data_nascimento=fake.date_of_birth(minimum_age=10, maximum_age=14),
        cpf=cpf,
        rg=fake.rg(),
        sexo=sexo,
        nacionalidade='Brasileira',
        naturalidade=fake.city(),
        certidao_numero='',
        certidao_livro='',
        tipo_sanguineo=choice(tipos_sanguineos),
        rua=fake.street_name(),
        numero=str(fake.building_number()),
        cep=fake.postcode(),
        bairro=fake.bairro(),
        cidade=fake.city(),
        estado=fake.estado_sigla(),
        email=fake.email(),
        telefone=fake.phone_number(),
        escola=escola
    )
    print(f"✅ Aluno criado: {aluno.nome} | Matrícula: {aluno.matricula}")
EOF

echo "✅ População concluída com sucesso!"
