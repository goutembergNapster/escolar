from django.db import models
from django.contrib.auth.models import AbstractUser, Group, Permission
from django.core.validators import RegexValidator
from django.core.exceptions import ValidationError
import uuid
from .utils import gerar_matricula_unica
from django.core.validators import MinValueValidator, MaxValueValidator

# Modelo de Usuário Customizado com a Role
class Escola(models.Model):
    nome = models.CharField(max_length=255, unique=True)
    cnpj = models.CharField(
        max_length=18,
        unique=True,
        validators=[RegexValidator(regex=r'^\d{14}$', message='CNPJ inválido')]
    )
    telefone = models.CharField(max_length=16, validators=[
        RegexValidator(regex=r'^\(?\d{2}\)?[\s-]?\d{4,5}-?\d{4}$', message='Telefone deve estar no formato (XX) XXXX-XXXX ou (XX) XXXXX-XXXX')
    ])
    email = models.EmailField(max_length=100)
    endereco = models.CharField(max_length=255)
    numero = models.CharField(max_length=10)
    complemento = models.CharField(max_length=255, blank=True, null=True)
    bairro = models.CharField(max_length=100)
    cidade = models.CharField(max_length=100)
    estado = models.CharField(max_length=2)
    site = models.CharField(max_length=200, blank=True, null=True)
    cep = models.CharField(max_length=9, default='00000000')

    def clean(self):
        if self.cnpj:
            self.cnpj = self.cnpj.replace('.', '').replace('/', '').replace('-', '')
        if Escola.objects.filter(cnpj=self.cnpj).exclude(id=self.id).exists():
            raise ValidationError("Este CNPJ já está cadastrado no sistema.")

    def __str__(self):
        return self.nome

class User(AbstractUser):
    ROLE_CHOICES = [
        ('professor', 'Professor'),
        ('diretor', 'Diretor'),
        ('coordenador', 'Coordenador'),
        ('secretaria', 'Secretária'),
        ('responsavel', 'Responsável'),
    ]

    cpf = models.CharField(max_length=11, unique=True, null=True, blank=True)  # <== ADICIONE ISSO
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='funcionario')
    escola = models.ForeignKey(Escola, on_delete=models.CASCADE, null=True, blank=True)
    senha_temporaria = models.BooleanField(default=False)
    groups = models.ManyToManyField(Group, related_name="home_user_groups", blank=True)
    user_permissions = models.ManyToManyField(Permission, related_name="home_user_permissions", blank=True)

    USERNAME_FIELD = 'cpf'
    REQUIRED_FIELDS = ['username', 'first_name', 'last_name']

    def __str__(self):
        return self.cpf or self.username

def gerar_matricula():
    return uuid.uuid4().hex[:10].upper()

class Disciplina(models.Model):
    nome = models.CharField(max_length=100)
    escola = models.ForeignKey(Escola, on_delete=models.CASCADE)

    def __str__(self):
        return self.nome

class Docente(models.Model):
    nome = models.CharField(max_length=100, default='')
    cpf = models.CharField(max_length=14, unique=True, default='')
    nascimento = models.DateField(default='1900-01-01')
    email = models.EmailField(default='')
    telefone = models.CharField(max_length=20, default='')
    cep = models.CharField(max_length=9, default='000000000')
    endereco = models.CharField(max_length=100, default='')
    numero = models.CharField(max_length=10, default='')
    complemento = models.CharField(max_length=100, blank=True, default='')
    bairro = models.CharField(max_length=50, default='Bairro')
    cidade = models.CharField(max_length=50, default='Cidade')
    estado = models.CharField(max_length=2, default='PE')
    cargo = models.CharField(max_length=50, default='Professor')
    disciplinas = models.ManyToManyField(Disciplina, blank=True)
    formacao = models.CharField(max_length=100, default='')
    experiencia = models.TextField(default='')
    sexo = models.CharField(max_length=50, default='Masculino')
    ativo = models.CharField(max_length=9, default='Sim')
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)
    escola = models.ForeignKey(Escola, on_delete=models.CASCADE, related_name='docentes', default=1)

    def __str__(self):
        disciplinas = ', '.join([d.nome for d in self.disciplinas.all()])
        return f"{self.nome} ({disciplinas})"

class Funcionario(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    cargo = models.CharField(max_length=100)
    departamento = models.CharField(max_length=100)
    data_admissao = models.DateField()
    escola = models.ForeignKey(Escola, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return f"{self.user.username} - {self.cargo}"

class Plantao(models.Model):
    id = models.AutoField(primary_key=True)
    data_inicio = models.DateField()
    hora_inicio = models.TimeField()
    data_termino = models.DateField()
    hora_termino = models.TimeField()
    professor_responsavel = models.ForeignKey(Docente, on_delete=models.SET_NULL, blank=True, null=True)
    especialidade = models.CharField(max_length=255)
    tipo_plantao = models.CharField(max_length=20)
    quantidade_horas = models.DecimalField(max_digits=5, decimal_places=2)
    valor = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=12)
    observacoes = models.TextField(blank=True, null=True)
    escola = models.ForeignKey(Escola, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return f'Plantão {self.tipo_plantao} - {self.professor_responsavel.user.username}'

class Aluno(models.Model):
    matricula = models.CharField(max_length=20, unique=True, default=gerar_matricula_unica)
    nome = models.CharField(max_length=255, default='')
    data_nascimento = models.DateField(blank=True, null=True)
    cpf = models.CharField(max_length=14, default='')
    rg = models.CharField(max_length=20, blank=True, null=True, default='')
    sexo = models.CharField(max_length=10, default='')
    nacionalidade = models.CharField(max_length=50, default='')
    naturalidade = models.CharField(max_length=50, default='')
    certidao_numero = models.CharField(max_length=50, blank=True, null=True, default='')
    certidao_livro = models.CharField(max_length=50, blank=True, null=True, default='')
    tipo_sanguineo = models.CharField(max_length=3, default='')
    rua = models.CharField(max_length=100, default='')
    numero = models.CharField(max_length=10, default='')
    cep = models.CharField(max_length=10, default='')
    bairro = models.CharField(max_length=50, default='')
    cidade = models.CharField(max_length=50, default='')
    estado = models.CharField(max_length=2, default='')
    email = models.EmailField(default='')
    telefone = models.CharField(max_length=20, default='')
    ativo = models.BooleanField(default=True)
    escola = models.ForeignKey(Escola, on_delete=models.CASCADE, null=True, blank=True)
    data_ingresso = models.DateField(null=True, blank=True)
    cor_raca = models.CharField(max_length=20, null=True, blank=True, choices=[
        ('branca','Branca'),
        ('preta','Preta'),
        ('parda','Parda'),
        ('amarela','Amarela'),
        ('indigena','Indígena'),
        ('nao_informado','Não informado'),
    ])
    responsavel_financeiro = models.CharField(max_length=10, null=True, blank=True, choices=[
        ('pai','Pai'),
        ('mae','Mãe'),
        ('outro','Outro'),
    ])
    situacao_familiar = models.CharField(max_length=12, null=True, blank=True, choices=[
        ('casados','Casados'),
        ('separados','Separados'),
        ('outros','Outros'),
    ])
    dispensa_ensino_religioso = models.BooleanField(default=False)
    forma_acesso = models.CharField(max_length=50, null=True, blank=True)
    SITUACAO_MATRICULA = [
        ("matricula", "Matrícula"),
        ("rematricula", "Rematrícula"),
        ("transferencia", "Transferência"),
    ]
    situacao_matricula = models.CharField(
        max_length=20, choices=SITUACAO_MATRICULA, blank=True, null=True
    )
    bolsa_familia = models.BooleanField(default=False)
    serie_ano = models.CharField(max_length=50, blank=True)  # ex: "5º Ano A"
    turno_aluno = models.CharField(max_length=20, blank=True)  # Manhã/Tarde/Noite

    # se quiser “fixar” uma turma principal (opcional)
    turma_principal = models.ForeignKey(
        "Turma", on_delete=models.SET_NULL, null=True, blank=True, related_name="alunos_principais"
    ) 
    
    def __str__(self):
        return f"{self.nome} - {self.matricula}"

class Responsavel(models.Model):
    aluno = models.OneToOneField(Aluno, on_delete=models.CASCADE)
    nome = models.CharField(max_length=255, default='')
    cpf = models.CharField(max_length=14, default='')
    parentesco = models.CharField(max_length=50, default='')
    telefone = models.CharField(max_length=20, default='')
    email = models.EmailField(default='')
    tipo = models.CharField(max_length=10, null=True, blank=True, choices=[
        ('pai','Pai'),
        ('mae','Mãe'),
        ('outro','Outro'),
    ])
    identidade = models.CharField(max_length=30, null=True, blank=True)
    escolaridade = models.CharField(max_length=50, null=True, blank=True)
    profissao = models.CharField(max_length=60, null=True, blank=True)

class Saude(models.Model):
    aluno = models.OneToOneField(Aluno, on_delete=models.CASCADE)
    possui_necessidade_especial = models.BooleanField(default=False)
    descricao_necessidade = models.TextField(blank=True, null=True, default='')
    usa_medicacao = models.BooleanField(default=False)
    quais_medicacoes = models.TextField(blank=True, null=True, default='')
    possui_alergia = models.BooleanField(default=False)
    descricao_alergia = models.TextField(blank=True, null=True, default='')

class TransporteEscolar(models.Model):
    aluno = models.OneToOneField(Aluno, on_delete=models.CASCADE)
    usa_transporte_escolar = models.BooleanField(default=False)
    trajeto = models.CharField(max_length=255, blank=True, null=True, default='')

class Autorizacoes(models.Model):
    aluno = models.OneToOneField(Aluno, on_delete=models.CASCADE)
    autorizacao_saida_sozinho = models.BooleanField(default=False)
    autorizacao_fotos_eventos = models.BooleanField(default=False)
    pessoa_autorizada_buscar = models.CharField(max_length=255, blank=True, null=True, default='')
    usa_transporte_publico = models.BooleanField(default=False)

class Turma(models.Model):
    nome = models.CharField(max_length=100)
    turno = models.CharField(max_length=20)
    ano = models.IntegerField()
    sala = models.CharField(max_length=20)
    descricao = models.TextField(blank=True)
    alunos = models.ManyToManyField('Aluno', blank=True, related_name='turmas')
    professores = models.ManyToManyField('Docente', blank=True, related_name='turmas')
    escola = models.ForeignKey(Escola, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return f"{self.nome} - {self.turno}"

class Nota(models.Model):
    aluno = models.ForeignKey('Aluno', on_delete=models.CASCADE, related_name='notas')
    disciplina = models.ForeignKey('Disciplina', on_delete=models.CASCADE)
    turma = models.ForeignKey('Turma', on_delete=models.CASCADE, null=True, blank=True)  # <-- Temporariamente opcional
    bimestre = models.IntegerField(choices=[
        (1, '1º Bimestre'),
        (2, '2º Bimestre'),
        (3, '3º Bimestre'),
        (4, '4º Bimestre')
    ])
    valor = models.DecimalField(max_digits=5, decimal_places=2)
    observacoes = models.TextField(blank=True, null=True)
    escola = models.ForeignKey('Escola', on_delete=models.CASCADE)

    class Meta:
        unique_together = ('aluno', 'disciplina', 'turma', 'bimestre', 'escola')

    def __str__(self):
        return f"{self.aluno.nome} - {self.disciplina.nome} - {self.bimestre}º Bim: {self.valor}"   
    
class TurmaDisciplina(models.Model):
    turma = models.ForeignKey('Turma', on_delete=models.CASCADE)
    disciplina = models.ForeignKey('Disciplina', on_delete=models.CASCADE)
    professor = models.ForeignKey('Docente', on_delete=models.CASCADE)
    escola = models.ForeignKey('Escola', on_delete=models.CASCADE, null=True)

    class Meta:
        unique_together = ('turma', 'disciplina', 'professor')

    def __str__(self):
        return f"{self.turma.nome} - {self.disciplina.nome} ({self.professor.nome})"
    
class Chamada(models.Model):
    data = models.DateField(auto_now_add=True)
    turma = models.ForeignKey('Turma', on_delete=models.CASCADE)
    disciplina = models.ForeignKey('Disciplina', on_delete=models.CASCADE)
    professor = models.ForeignKey('Docente', on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.data} - {self.turma.nome} - {self.disciplina.nome}"

    class Meta:
        unique_together = ('data', 'turma', 'disciplina', 'professor')

class Presenca(models.Model):
    chamada = models.ForeignKey('Chamada', on_delete=models.CASCADE)
    aluno = models.ForeignKey('Aluno', on_delete=models.CASCADE)
    presente = models.BooleanField(default=True)
    observacao = models.TextField(blank=True)

    def __str__(self):
        return f"{self.aluno.nome} - {self.chamada.data} - {'Presente' if self.presente else 'Ausente'}"

    class Meta:
        unique_together = ('chamada', 'aluno')
