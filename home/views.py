from django.shortcuts import render
from .models import Escola
from django.http import JsonResponse
import re
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect
from .forms import EscolaForm
import json
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from .models import Docente
from django.contrib.auth import get_user_model, logout, login, update_session_auth_hash
from django.utils.dateparse import parse_date
from django.views.decorators.csrf import ensure_csrf_cookie
from .models import Aluno, Responsavel, Saude, TransporteEscolar, Autorizacoes, Turma, Disciplina, Funcionario, Nota, TurmaDisciplina 
from home.utils import gerar_matricula_unica
from datetime import datetime
from django.db.models.functions import Substr, Cast
from django.db.models import IntegerField
from django.core.serializers.json import DjangoJSONEncoder
from django.views.decorators.http import require_GET
from django.db.models import Q
from home.decorators import role_required
from django.contrib.auth.forms import AuthenticationForm
from home.utils_user import criar_usuario_com_cpf
from django.db import transaction
from django.contrib import messages
import pandas as pd
from collections import defaultdict
from django.db.models import Avg
from django.http import HttpResponseNotFound

User = get_user_model()

def index(request):
    return render(
        request,
        'plantaopro/pages/index.html'
    )


def cadastro_escola(request):
    form = EscolaForm()
    return render(request, 'plantaopro/pages/cadastrar_escola.html', {'form': form})


def cadastrar_escola_banco(request):
    if request.method == 'POST' and request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        try:
            data = json.loads(request.body)

            nome = data.get('schoolName')
            cnpj = data.get('schoolCnpj')
            telefone = data.get('schoolPhone')
            email = data.get('schoolEmail')
            endereco = data.get('schoolStreet')
            numero = data.get('schoolNumber')
            complemento = data.get('schoolComplement')
            bairro = data.get('schoolNeighborhood')
            cidade = data.get('schoolCity')
            estado = data.get('schoolState')
            site = data.get('schoolWebsite')
            cep = data.get('schoolCep')

            if Escola.objects.filter(cnpj=cnpj, escola=request.user.escola).exists():
                return JsonResponse({'success': False, 'error': 'CNPJ já cadastrado.'})

            Escola.objects.create(
                nome=nome,
                cnpj=cnpj,
                telefone=telefone,
                email=email,
                endereco=endereco,
                numero=numero,
                complemento=complemento,
                bairro=bairro,
                cidade=cidade,
                estado=estado,
                site=site,
                cep=cep
            )

            return JsonResponse({'success': True})
        except Exception as e:
            return JsonResponse({'success': False, 'error': f'Erro interno: {str(e)}'})

    return JsonResponse({'success': False, 'error': 'Método não permitido'})

@login_required
@role_required(['diretor', 'coordenador'])
def cadastro_aluno(request):
    cadastro_aluno = Escola.objects.all()  
    context = {
        'cadastro_aluno': cadastro_aluno  
    }
    return render(request, 'plantaopro/pages/registrar_aluno.html', context)

@login_required
@role_required(['diretor', 'coordenador'])
def cadastro_funcionarios(request):
    cadastro_funcionario = Escola.objects.all()  
    context = {
        'cadastro_funcionario': cadastro_funcionario 
    }
    return render(request, 'plantaopro/pages/registrar_funcionarios.html', context)

@login_required
@role_required(['diretor', 'coordenador'])
def cadastro_turma(request):
    escola = request.user.escola
    disciplinas = Disciplina.objects.filter(escola=escola)

    context = {
        'disciplinas': disciplinas
    }
    return render(request, 'plantaopro/pages/registrar_turma.html', context)


@login_required
@role_required(['diretor', 'coordenador'])
def cadastro_professor(request):
    escolas = Escola.objects.all()
    disciplinas = Disciplina.objects.filter(escola=request.user.escola)
    context = {
        'cadastro_professor': escolas,
        'disciplinas': disciplinas,
    }
    return render(request, 'plantaopro/pages/registrar_professor.html', context)

@csrf_exempt
@require_POST
def buscar_cnpj(request):
    body = json.loads(request.body)
    cnpj = body.get('cnpj')

    if not validar_cnpj(cnpj):
        return JsonResponse({"error": "CNPJ inválido"}, status=400)

    try:
        escola = Escola.objects.get(cnpj=cnpj, escola=request.user.escola)
        return JsonResponse({"exists": True, "escola": {
            "schoolName": escola.nome,
            "schoolPhone": escola.telefone,
            "schoolEmail": escola.email,
            "schoolStreet": escola.endereco,
            "schoolNumber": escola.numero,
            "schoolComplement": escola.complemento,
            "schoolNeighborhood": escola.bairro,
            "schoolCity": escola.cidade,
            "schoolState": escola.estado,
            "schoolWebsite": escola.site,
        }})
    except Escola.DoesNotExist:
        return JsonResponse({"exists": False})

def validar_cnpj(cnpj):
    cnpj = re.sub(r'\D', '', cnpj)
    if len(cnpj) != 14 or cnpj in [s * 14 for s in "0123456789"]:
        return False
    def calc_digito(cnpj, peso):
        soma = sum(int(cnpj[i]) * peso[i] for i in range(len(peso)))
        resto = soma % 11
        return '0' if resto < 2 else str(11 - resto)
    peso1 = [5, 4, 3, 2, 9, 8, 7, 6, 5, 4, 3, 2]
    peso2 = [6] + peso1
    dig1 = calc_digito(cnpj[:12], peso1)
    dig2 = calc_digito(cnpj[:12] + dig1, peso2)
    return cnpj[-2:] == dig1 + dig2


@csrf_exempt
@transaction.atomic
def cadastrar_professor_banco(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)

            cpf = data.get('doctorCpf', '').strip().replace('.', '').replace('-', '')
            nome = data.get('doctorName', '').strip()
            nascimento = parse_date(data.get('birthdate'))
            email = data.get('email', '').strip()
            telefone = data.get('phone', '').strip()
            cep = data.get('cep', '').strip()
            endereco = data.get('address', '').strip()
            numero = data.get('number', '').strip()
            complemento = data.get('complement', '').strip()
            bairro = data.get('bairro', '').strip()
            cidade = data.get('city', '').strip()
            estado = data.get('state', '').strip()
            cargo = data.get('cargo', '').strip()
            formacao = data.get('formacao', '').strip()
            experiencia = data.get('experiencia', '').strip()
            ativo = data.get('ativo', 'True') == 'True'
            senha = data.get('senha')

            escola_usuario = getattr(request.user, 'escola', None)
            if not escola_usuario:
                return JsonResponse({'success': False, 'error': 'Usuário não está vinculado a nenhuma escola.'}, status=403)

            if not senha:
                return JsonResponse({'success': False, 'error': 'Senha temporária ausente.'}, status=400)

            if User.objects.filter(cpf=cpf, escola=escola_usuario).exists():
                return JsonResponse({'success': False, 'error': 'Usuário já cadastrado.'}, status=400)

            # Trata nome para o User
            nome_completo = nome.strip()
            partes = nome_completo.split()
            first = partes[0]
            last = ' '.join(partes[1:]) if len(partes) > 1 else ''

            # Cria o usuário
            usuario = User(
                username=cpf,
                cpf=cpf,
                email=email,
                first_name=first,
                last_name=last,
                role=cargo,
                is_active=True,
                escola=escola_usuario,
                senha_temporaria=True
            )
            usuario.set_password(senha)
            usuario.save()

            docente = Docente.objects.create(
                user=usuario,
                nome=nome,
                cpf=cpf,
                nascimento=nascimento,
                email=email,
                telefone=telefone,
                cep=cep,
                endereco=endereco,
                numero=numero,
                complemento=complemento,
                bairro=bairro,
                cidade=cidade,
                estado=estado,
                cargo=cargo,
                formacao=formacao,
                experiencia=experiencia,
                ativo=ativo,
                escola=escola_usuario
            )

            # ❌ Nenhum vínculo com disciplinas neste momento

            return JsonResponse({'success': True, 'senha': senha})

        except Exception as e:
            transaction.set_rollback(True)
            return JsonResponse({'success': False, 'error': f'Erro interno: {str(e)}'}, status=500)

    return JsonResponse({'success': False, 'error': 'Método não permitido'}, status=405)


@login_required
@role_required(['diretor', 'coordenador'])
def listar_professores(request):
    professores = Docente.objects.select_related('user').filter(escola=request.user.escola).order_by('nome')
    return render(request, 'plantaopro/pages/listar_professores.html', {
        'professores': professores
    })

@csrf_exempt
def editar_professor(request, prof_id):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            professor = Docente.objects.get(id=prof_id, escola=request.user.escola)

            professor.nome = data.get('nome', professor.nome)
            professor.disciplina = data.get('disciplina', professor.disciplina)
            professor.save()

            return JsonResponse({'success': True})
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)})

    return JsonResponse({'success': False, 'error': 'Método inválido'})

@csrf_exempt
@login_required
def alternar_status_professor(request, prof_id):
    if request.method == 'POST':
        try:
            professor = Docente.objects.get(id=prof_id, escola=request.user.escola)

            professor.ativo = not professor.ativo
            professor.save()

            return JsonResponse({'success': True, 'novo_status': professor.ativo})

        except Docente.DoesNotExist:
            return JsonResponse({'success': False, 'error': 'Professor não encontrado ou sem permissão'}, status=404)

        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)}, status=500)

    return JsonResponse({'success': False, 'error': 'Método inválido'}, status=405)

@csrf_exempt
def to_bool(value):
    return str(value).lower() in ['true', '1', 'sim']


@csrf_exempt
@login_required
def salvar_aluno(request):
    if request.method == 'POST':
        data = json.loads(request.body)

        # 🛡️ Validação dos campos obrigatórios
        campos_obrigatorios = ['nome', 'data_nascimento', 'cpf', 'email', 'telefone', 'rua', 'numero', 'bairro', 'cidade', 'estado']
        for campo in campos_obrigatorios:
            if not data.get(campo):
                return JsonResponse({'status': 'erro', 'mensagem': f'O campo "{campo}" é obrigatório.'}, status=400)

        # Geração da matrícula, se necessário
        if not data.get('matricula'):
            ano = datetime.now().year
            ultimo = (
                Aluno.objects
                .filter(matricula__startswith=str(ano))
                .annotate(numero_final=Cast(Substr('matricula', -4, 4), IntegerField()))
                .order_by('-numero_final')
                .first()
            )
            ultimo_numero = ultimo.numero_final if ultimo else 0
            novo_numero = ultimo_numero + 1
            data['matricula'] = f"{ano}{novo_numero:04d}"

        try:
            data_nascimento_str = data.get('data_nascimento')
            data_nascimento = datetime.strptime(data_nascimento_str, '%Y-%m-%d').date() if data_nascimento_str else None

            aluno = Aluno.objects.create(
                matricula=data.get('matricula', ''),
                nome=data.get('nome', ''),
                data_nascimento=data_nascimento,
                cpf=data.get('cpf', ''),
                rg=data.get('rg', ''),
                sexo=data.get('sexo', ''),
                nacionalidade=data.get('nacionalidade', ''),
                naturalidade=data.get('naturalidade', ''),
                certidao_numero=data.get('certidao_numero', ''),
                certidao_livro=data.get('certidao_livro', ''),
                tipo_sanguineo=data.get('tipo_sanguineo', ''),
                rua=data.get('rua', ''),
                numero=data.get('numero', ''),
                cep=data.get('cep', ''),
                bairro=data.get('bairro', ''),
                cidade=data.get('cidade', ''),
                estado=data.get('estado', ''),
                email=data.get('email', ''),
                telefone=data.get('telefone', ''),
                escola=request.user.escola  # ⬅️ Associar escola
            )

            Responsavel.objects.create(
                aluno=aluno,
                nome=data.get('responsavel_nome', ''),
                cpf=data.get('responsavel_cpf', ''),
                parentesco=data.get('responsavel_parentesco', ''),
                telefone=data.get('responsavel_telefone', ''),
                email=data.get('responsavel_email', '')
            )

            Saude.objects.create(
                aluno=aluno,
                possui_necessidade_especial=to_bool(data.get('possui_necessidade_especial')),
                descricao_necessidade=data.get('descricao_necessidade', ''),
                usa_medicacao=to_bool(data.get('usa_medicacao')),
                quais_medicacoes=data.get('quais_medicacoes', ''),
                possui_alergia=to_bool(data.get('possui_alergia')),
                descricao_alergia=data.get('descricao_alergia', '')
            )

            TransporteEscolar.objects.create(
                aluno=aluno,
                usa_transporte_escolar=to_bool(data.get('usa_transporte_escolar')),
                trajeto=data.get('trajeto', '')
            )

            Autorizacoes.objects.create(
                aluno=aluno,
                autorizacao_saida_sozinho=to_bool(data.get('autorizacao_saida_sozinho')),
                autorizacao_fotos_eventos=to_bool(data.get('autorizacao_fotos_eventos')),
                pessoa_autorizada_buscar=data.get('pessoa_autorizada_buscar', '')
            )

            if 'matricula_gerada' in request.session:
                del request.session['matricula_gerada']

            return JsonResponse({'status': 'sucesso', 'aluno_id': aluno.id, 'matricula': aluno.matricula})

        except Exception as e:
            return JsonResponse({'status': 'erro', 'mensagem': str(e)}, status=400)

    return JsonResponse({'mensagem': 'Método não permitido'}, status=405)


@login_required
@role_required(['diretor', 'coordenador'])
def cadastrar_aluno(request):
    # Sempre gera nova matrícula ao carregar a página
    request.session['matricula_gerada'] = gerar_matricula_unica()

    return render(request, 'plantaopro/pages/registrar_aluno.html', {
        'matricula': request.session['matricula_gerada']
    })


@csrf_exempt
def editar_aluno(request, aluno_id):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            aluno = Aluno.objects.get(id=aluno_id, escola=request.user.escola)

            # Atualiza dados principais do aluno
            aluno.nome = data.get('nome', aluno.nome)
            aluno.email = data.get('email', aluno.email)
            aluno.telefone = data.get('telefone', aluno.telefone)
            aluno.save()

            # Atualiza dados do responsável (se existirem)
            responsavel = Responsavel.objects.filter(aluno=aluno, escola=request.user.escola).first()
            if responsavel:
                responsavel.nome = data.get('responsavel_nome', responsavel.nome)
                responsavel.cpf = data.get('responsavel_cpf', responsavel.cpf)
                responsavel.parentesco = data.get('responsavel_parentesco', responsavel.parentesco)
                responsavel.telefone = data.get('responsavel_telefone', responsavel.telefone)
                responsavel.email = data.get('responsavel_email', responsavel.email)
                responsavel.save()

            # Atualiza dados de saúde
            saude = Saude.objects.filter(aluno=aluno, escola=request.user.escola).first()
            if saude:
                saude.possui_necessidade_especial = data.get('possui_necessidade_especial', saude.possui_necessidade_especial)
                saude.descricao_necessidade = data.get('descricao_necessidade', saude.descricao_necessidade)
                saude.usa_medicacao = data.get('usa_medicacao', saude.usa_medicacao)
                saude.quais_medicacoes = data.get('quais_medicacoes', saude.quais_medicacoes)
                saude.possui_alergia = data.get('possui_alergia', saude.possui_alergia)
                saude.descricao_alergia = data.get('descricao_alergia', saude.descricao_alergia)
                saude.save()

            # Atualiza transporte escolar
            transporte = TransporteEscolar.objects.filter(aluno=aluno, escola=request.user.escola).first()
            if transporte:
                transporte.usa_transporte_escolar = data.get('usa_transporte_escolar', transporte.usa_transporte_escolar)
                transporte.trajeto = data.get('trajeto', transporte.trajeto)
                transporte.save()

            # Atualiza autorizações
            autorizacoes = Autorizacoes.objects.filter(aluno=aluno, escola=request.user.escola).first()
            if autorizacoes:
                autorizacoes.autorizacao_saida_sozinho = data.get('autorizacao_saida_sozinho', autorizacoes.autorizacao_saida_sozinho)
                autorizacoes.autorizacao_fotos_eventos = data.get('autorizacao_fotos_eventos', autorizacoes.autorizacao_fotos_eventos)
                autorizacoes.pessoa_autorizada_buscar = data.get('pessoa_autorizada_buscar', autorizacoes.pessoa_autorizada_buscar)
                autorizacoes.save()

            return JsonResponse({'success': True})
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)})

    return JsonResponse({'success': False, 'error': 'Método inválido'})


@csrf_exempt
def alternar_status_aluno(request, aluno_id):
    if request.method == 'POST':
        try:
            aluno = Aluno.objects.get(id=aluno_id, escola=request.user.escola)
            aluno.ativo = not aluno.ativo
            aluno.save()
            return JsonResponse({'success': True})
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)})

    return JsonResponse({'success': False, 'error': 'Método inválido'})

def listar_alunos(request):
    alunos = Aluno.objects.filter(escola=request.user.escola)
    lista = []

    for aluno in alunos:
        responsavel = getattr(aluno, 'responsavel', None)
        saude = getattr(aluno, 'saude', None)
        transporte = getattr(aluno, 'transporteescolar', None)
        autorizacoes = getattr(aluno, 'autorizacoes', None)

        lista.append({
            'id': aluno.id,
            'matricula': aluno.matricula,
            'nome': aluno.nome,
            'cpf': aluno.cpf,
            'email': aluno.email,
            'telefone': aluno.telefone,
            'ativo': aluno.ativo,

            # Responsável
            'responsavel_nome': responsavel.nome if responsavel else '',
            'responsavel_cpf': responsavel.cpf if responsavel else '',
            'responsavel_parentesco': responsavel.parentesco if responsavel else '',
            'responsavel_telefone': responsavel.telefone if responsavel else '',
            'responsavel_email': responsavel.email if responsavel else '',

            # Saúde
            'possui_necessidade_especial': saude.possui_necessidade_especial if saude else False,
            'descricao_necessidade': saude.descricao_necessidade if saude else '',
            'usa_medicacao': saude.usa_medicacao if saude else False,
            'quais_medicacoes': saude.quais_medicacoes if saude else '',
            'possui_alergia': saude.possui_alergia if saude else False,
            'descricao_alergia': saude.descricao_alergia if saude else '',

            # Transporte
            'usa_transporte_escolar': transporte.usa_transporte_escolar if transporte else False,
            'trajeto': transporte.trajeto if transporte else '',

            # Autorizações
            'autorizacao_saida_sozinho': autorizacoes.autorizacao_saida_sozinho if autorizacoes else False,
            'autorizacao_fotos_eventos': autorizacoes.autorizacao_fotos_eventos if autorizacoes else False,
            'pessoa_autorizada_buscar': autorizacoes.pessoa_autorizada_buscar if autorizacoes else '',
        })

    context = {
        'alunos_json': json.dumps(lista, cls=DjangoJSONEncoder)
    }
    return render(request, 'plantaopro/pages/listar_alunos.html', context)

@csrf_exempt  # ou use um decorator de CSRF seguro se for AJAX autenticado
@require_POST
def buscar_pessoa(request):
    try:
        data = json.loads(request.body)
        nome = data.get("nome", "").strip()
        tipo = data.get("tipo", "").lower()

        if not nome or tipo not in ["aluno", "professor"]:
            return JsonResponse({"error": "Parâmetros inválidos"}, status=400)

        if tipo == "professor":
            professores = Docente.objects.filter(nome__icontains=nome, escola=request.user.escola).order_by("nome")
            resultados = [
                {"nome": p.nome, "disciplina": p.disciplina or "Disciplina não informada"} for p in professores
            ]
        else:
            alunos = Aluno.objects.filter(nome__icontains=nome, escola=request.user.escola).order_by("nome")
            resultados = [{"nome": a.nome} for a in alunos]

        return JsonResponse({"resultados": resultados})
    
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)

@require_GET
def autocomplete_pessoa(request):
    nome = request.GET.get('nome', '').strip()
    tipo = request.GET.get('tipo', '').strip()

    resultados = []

    if not nome or tipo not in ['aluno', 'professor']:
        return JsonResponse({'resultados': []})

    if tipo == 'aluno':
        alunos = Aluno.objects.filter(nome__icontains=nome, escola=request.user.escola)[:10]
        for aluno in alunos:
            resultados.append({
                'nome': aluno.nome,
                'id': aluno.id,
                'tipo': 'aluno'
            })

    elif tipo == 'professor':
        professores = Docente.objects.filter(nome__icontains=nome, escola=request.user.escola).prefetch_related('disciplinas')[:10]
        for prof in professores:
            nomes_disciplinas = [d.nome for d in prof.disciplinas.all()]
            resultados.append({
                'nome': prof.nome,
                'id': prof.id,
                'tipo': 'professor',
                'disciplina': ', '.join(nomes_disciplinas) if nomes_disciplinas else 'Sem disciplina'
            })

    return JsonResponse({'resultados': resultados})


@csrf_exempt
def criar_turma(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)

            nome = data.get('nome', '').strip()
            turno = data.get('turno', '').strip()
            ano = data.get('ano')
            sala = data.get('sala', '').strip()
            descricao = data.get('descricao', '').strip()
            professor_id = data.get('professor_id', '')
            disciplina_id = data.get('disciplina_id', '')
            alunos_ids = data.get('alunos_ids', [])

            if not nome or not turno or not ano or not sala:
                return JsonResponse({'success': False, 'mensagem': 'Preencha todos os campos obrigatórios.'})

            # Garante que a turma pertença à escola do usuário
            escola = request.user.escola
            turma = Turma.objects.create(
                nome=nome,
                turno=turno,
                ano=ano,
                sala=sala,
                descricao=descricao,
                escola=escola
            )

            if professor_id and disciplina_id:
                professor = Docente.objects.filter(id=professor_id, escola=escola).first()
                disciplina = Disciplina.objects.filter(id=disciplina_id, escola=escola).first()

                if professor and disciplina:
                    # Cria relacionamento TurmaDisciplina
                    TurmaDisciplina.objects.create(
                        turma=turma,
                        professor=professor,
                        disciplina=disciplina,
                        escola=escola
                    )

            if isinstance(alunos_ids, list):
                alunos = Aluno.objects.filter(id__in=alunos_ids, escola=escola)
                turma.alunos.add(*alunos)

            return JsonResponse({'success': True, 'mensagem': 'Turma criada com sucesso!'})

        except Exception as e:
            return JsonResponse({'success': False, 'mensagem': f'Erro ao criar turma: {str(e)}'})

    return JsonResponse({'success': False, 'mensagem': 'Método não permitido'}, status=405)

@login_required
@role_required(['diretor', 'coordenador'])
def formulario_criar_turma(request):
    escola = request.user.escola
    disciplinas = Disciplina.objects.filter(escola=escola).order_by('nome')

    return render(request, 'plantaopro/pages/criar_turma.html', {
        'disciplinas': disciplinas
    })


@login_required
@role_required(['diretor', 'coordenador'])
def impressao_dados(request):
    tipo = request.GET.get('tipo', 'turmas')
    turma_id = request.GET.get('turma')
    professor_id = request.GET.get('professor')
    dados = []

    if tipo == 'turmas':
        turmas = Turma.objects.prefetch_related('alunos', 'professores')
        if turma_id:
            turmas = turmas.filter(id=turma_id)
        if professor_id:
            turmas = turmas.filter(professores__id=professor_id)

        dados = [{
            'nome': t.nome,
            'sala': t.sala,
            'turno': t.turno,
            'ano': t.ano,
            'professor': ', '.join([p.nome for p in t.professores.all()]) if t.professores.exists() else '—',
            'qtd_alunos': t.alunos.count()
        } for t in turmas]

    elif tipo == 'alunos':
        alunos = Aluno.objects.select_related('responsavel').prefetch_related('turmas')
        if turma_id:
            alunos = alunos.filter(turmas__id=turma_id)
        if professor_id:
            alunos = alunos.filter(turmas__professores__id=professor_id)

        dados = [{
            'nome': a.nome,
            'cpf': a.cpf,
            'turma': ', '.join([turma.nome for turma in a.turmas.all()]) if a.turmas.exists() else '—',
            'telefone': a.telefone,
            'responsavel': a.responsavel.nome if a.responsavel else '—'
        } for a in alunos]

    elif tipo == 'professores':
        professores = Docente.objects.filter(escola=request.user.escola).prefetch_related("disciplinas")
        dados = [{
            'nome': p.nome,
            'cpf': p.cpf,
            'disciplinas': ', '.join([d.nome for d in p.disciplinas.all()]),
            'email': p.email,
            'cargo': p.cargo
        } for p in professores]

    elif tipo == 'funcionarios':
        funcionarios = Funcionario.objects.filter(escola=request.user.escola)
        dados = [{
            'nome': f.nome,
            'cpf': f.cpf,
            'cargo': f.cargo,
            'telefone': f.telefone,
            'email': f.email
        } for f in funcionarios]

    # Para popular os selects de filtro
    turmas_disponiveis = Turma.objects.filter(escola=request.user.escola)
    professores_disponiveis = Docente.objects.filter(escola=request.user.escola)

    context = {
        'tipo': tipo,
        'dados': dados,
        'turmas_disponiveis': turmas_disponiveis,
        'professores_disponiveis': professores_disponiveis,
        'turma_id': turma_id,
        'professor_id': professor_id,
    }
    return render(request, 'plantaopro/pages/print.html', context)

@csrf_exempt  # necessário para o uso com fetch (a menos que use CSRF token no cabeçalho)
@login_required
@role_required(['professor', 'diretor', 'coordenador'])
@require_POST
def lancar_notas(request):
    try:
        dados = json.loads(request.body)
        turma_id = dados.get("turma_id")
        disciplina_id = dados.get("disciplina_id")
        notas = dados.get("notas", {})  # notas é um dicionário: { aluno_id: { nota1: 8.5, nota2: 7.0, ... } }

        escola = request.user.escola
        turma = Turma.objects.get(id=turma_id, escola=escola)
        disciplina = Disciplina.objects.get(id=disciplina_id, escola=escola)

        for aluno_id_str, notas_aluno in notas.items():
            try:
                aluno_id = int(aluno_id_str)
                aluno = Aluno.objects.get(id=aluno_id, escola=escola)

                for bimestre_key, valor in notas_aluno.items():
                    try:
                        bimestre = int(bimestre_key.replace('nota', ''))
                        valor_float = float(valor)

                        Nota.objects.update_or_create(
                            aluno=aluno,
                            disciplina=disciplina,
                            turma=turma,
                            escola=escola,
                            bimestre=bimestre,
                            defaults={'valor': valor_float}
                        )
                    except (ValueError, TypeError):
                        continue  # ignora se valor inválido ou bimestre errado

            except (Aluno.DoesNotExist, ValueError):
                continue

        return JsonResponse({"mensagem": "Notas salvas com sucesso."})
    except Exception as e:
        return JsonResponse({"erro": f"Erro ao processar: {str(e)}"}, status=400)


@login_required
@role_required(['professor', 'diretor', 'coordenador'])
def registrar_notas(request):
    user = request.user
    turma_id = request.GET.get('turma')
    disciplina_id = request.GET.get('disciplina')

    escola = user.escola

    if hasattr(user, 'docente') and user.role == 'professor':
        relacoes = TurmaDisciplina.objects.filter(
            professor=user.docente,
            turma__escola=escola
        ).select_related('turma', 'disciplina')
    else:
        relacoes = TurmaDisciplina.objects.filter(
            turma__escola=escola
        ).select_related('turma', 'disciplina')

    turmas = list({rel.turma for rel in relacoes})
    disciplinas = list({rel.disciplina for rel in relacoes})

    alunos = []
    notas_dict = {}

    if turma_id and disciplina_id:
        turma = get_object_or_404(Turma, id=turma_id, escola=escola)
        disciplina = get_object_or_404(Disciplina, id=disciplina_id, escola=escola)
        alunos = turma.alunos.all().order_by('nome')

        # Busca notas já lançadas
        for aluno in alunos:
            notas = Nota.objects.filter(
                aluno=aluno,
                disciplina=disciplina,
                turma=turma,
                escola=escola
            )
            notas_dict[aluno.id] = {f"nota{n.bimestre}": n.valor for n in notas}

    context = {
        'turmas': turmas,
        'disciplinas': disciplinas,
        'alunos': alunos,
        'turma_id': turma_id or '',
        'disciplina_id': disciplina_id or '',
        'notas': notas_dict
    }
    return render(request, 'plantaopro/pages/registrar_notas.html', context)

def login_view(request):
    if request.user.is_authenticated:
        return redirect('index')

    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)

            if user.senha_temporaria:
                return redirect('trocar_senha')

            if user.is_superuser or (hasattr(user, 'escola') and user.escola):
                return redirect('index')
            else:
                return redirect('usuario_sem_escola')
    else:
        form = AuthenticationForm()

    return render(request, 'login.html', {'form': form})


def logout_view(request):
    logout(request)
    return redirect('login')

@csrf_exempt
def cadastrar_funcionario_banco(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)

            nome = data.get('nome', '').strip()
            cpf = data.get('cpf', '').strip()
            rg = data.get('rg', '').strip()
            sexo = data.get('sexo', '').strip()
            data_nascimento = parse_date(data.get('data_nascimento'))
            estado_civil = data.get('estado_civil', '').strip()
            escolaridade = data.get('escolaridade', '').strip()
            turno_trabalho = data.get('turno_trabalho', '').strip()
            carga_horaria = data.get('carga_horaria', '').strip()
            tipo_vinculo = data.get('tipo_vinculo', '').strip()
            observacoes = data.get('observacoes', '').strip()
            cep = data.get('cep', '').strip()
            endereco = data.get('endereco', '').strip()
            numero = data.get('numero', '').strip()
            complemento = data.get('complemento', '').strip()
            bairro = data.get('bairro', '').strip()
            cidade = data.get('cidade', '').strip()
            estado = data.get('estado', '').strip()
            telefone = data.get('telefone', '').strip()
            email = data.get('email', '').strip()
            cargo = data.get('cargo', '').strip()
            ativo = to_bool(data.get('ativo', 'True'))

            funcionario = Funcionario.objects.create(
                nome=nome,
                cpf=cpf,
                rg=rg,
                sexo=sexo,
                data_nascimento=data_nascimento,
                estado_civil=estado_civil,
                escolaridade=escolaridade,
                turno_trabalho=turno_trabalho,
                carga_horaria=carga_horaria,
                tipo_vinculo=tipo_vinculo,
                observacoes=observacoes,
                cep=cep,
                endereco=endereco,
                numero=numero,
                complemento=complemento,
                bairro=bairro,
                cidade=cidade,
                estado=estado,
                telefone=telefone,
                email=email,
                cargo=cargo,
                ativo=ativo
            )

            # Criação do usuário caso cargo seja "secretaria"
            if cargo.lower() == 'secretaria':
                criar_usuario_com_cpf(
                    cpf=cpf,
                    senha=data.get('senha', 'senha@123'),
                    role='secretaria',
                    escola=None,
                    email=email,
                    is_staff=True
                )

            return JsonResponse({'success': True})

        except Exception as e:
            return JsonResponse({'success': False, 'error': f'Erro ao cadastrar funcionário: {str(e)}'})

    return JsonResponse({'success': False, 'error': 'Método não permitido'}, status=405)



@login_required
@role_required(['diretor', 'coordenador'])
def importar_alunos(request):
    if request.method == 'POST' and request.FILES.get('arquivo'):
        arquivo = request.FILES['arquivo']

        try:
            df = pd.read_excel(arquivo)

            obrigatorios = ['nome', 'cpf', 'data_nascimento', 'email', 'telefone', 'cep', 'rua', 'numero', 'bairro', 'cidade', 'estado']
            for campo in obrigatorios:
                if campo not in df.columns:
                    messages.error(request, f"O campo obrigatório '{campo}' não foi encontrado na planilha.")
                    return redirect('importar_alunos')

            criados = 0
            ignorados = 0

            with transaction.atomic():
                for _, row in df.iterrows():
                    cpf = str(row.get('cpf')).replace('.', '').replace('-', '').strip()
                    if Aluno.objects.filter(cpf=cpf, escola=request.user.escola).exists():
                        ignorados += 1
                        continue

                    data_nasc = row.get('data_nascimento')
                    if isinstance(data_nasc, str):
                        data_nasc = datetime.strptime(data_nasc, "%Y-%m-%d")

                    aluno = Aluno.objects.create(
                        nome=row.get('nome', '').strip(),
                        cpf=cpf,
                        data_nascimento=data_nasc,
                        email=row.get('email', '').strip(),
                        telefone=row.get('telefone', '').strip(),
                        cep=row.get('cep', '').strip(),
                        rua=row.get('rua', '').strip(),
                        numero=str(row.get('numero', '')).strip(),
                        bairro=row.get('bairro', '').strip(),
                        cidade=row.get('cidade', '').strip(),
                        estado=row.get('estado', '').strip()
                    )

                    if row.get('responsavel_nome'):
                        Responsavel.objects.create(
                            aluno=aluno,
                            nome=row.get('responsavel_nome', '').strip(),
                            cpf=str(row.get('responsavel_cpf', '')).strip(),
                            telefone=row.get('responsavel_telefone', '').strip(),
                            email=row.get('responsavel_email', '').strip()
                        )

                    criados += 1

            messages.success(request, f"✅ {criados} aluno(s) importado(s) com sucesso. {ignorados} já existiam.")
        except Exception as e:
            messages.error(request, f"Erro ao processar a planilha: {str(e)}")

        return redirect('importar_alunos')

    return render(request, 'plantaopro/pages/importar_alunos.html')

@login_required
def verificar_senha_temporaria(request):
    if request.user.senha_temporaria:
        return render(request, 'plantaopro/pages/trocar_senha.html')
    return redirect('index')

@csrf_exempt
@login_required
def trocar_senha_api(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            nova = data.get('nova_senha')
            confirmar = data.get('nova_senha_confirmar')

            if not nova or nova != confirmar:
                return JsonResponse({'success': False, 'error': 'Senhas não coincidem'}, status=400)

            request.user.set_password(nova)
            request.user.senha_temporaria = False
            request.user.save()
            update_session_auth_hash(request, request.user)

            return JsonResponse({'success': True})
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)}, status=500)

    return JsonResponse({'success': False, 'error': 'Método não permitido'}, status=405)

@login_required
@role_required(['diretor', 'coordenador'])
def listar_turmas_para_boletim(request):
    turmas = Turma.objects.filter(escola=request.user.escola)
    alunos = []

    turma_id = request.GET.get('turma')
    if turma_id:
        alunos = Aluno.objects.filter(turmas__id=turma_id, escola=request.user.escola)

    return render(request, 'plantaopro/pages/listar_turmas_boletim.html', {
        'turmas': turmas,
        'alunos': alunos,
        'turma_id': turma_id
    })


@login_required
@role_required(['diretor', 'coordenador'])
def visualizar_boletim(request, aluno_id):
    aluno = get_object_or_404(Aluno, pk=aluno_id)
    turma_id = request.GET.get("turma")

    # Se turma for passada, filtra as notas por ela
    if turma_id:
        notas = Nota.objects.filter(
            aluno=aluno,
            escola=request.user.escola,
            turma_id=turma_id
        ).select_related('disciplina')
    else:
        # fallback se vier direto pela URL
        notas = Nota.objects.filter(
            aluno=aluno,
            escola=request.user.escola
        ).select_related('disciplina')

    # Organiza as notas no formato {disciplina: {1: nota, 2: nota, ...}}
    from collections import defaultdict

    boletim = defaultdict(lambda: {"1": None, "2": None, "3": None, "4": None, "obs": "", "media": None})

    for nota in notas:
        nome_disciplina = nota.disciplina.nome
        boletim[nome_disciplina][str(nota.bimestre)] = nota.valor
        if nota.observacoes:
            boletim[nome_disciplina]["obs"] = nota.observacoes

    for dados in boletim.values():
        notas_validas = [v for k, v in dados.items() if k in ['1', '2', '3', '4'] and v is not None]
        if notas_validas:
            dados["media"] = round(sum(notas_validas) / len(notas_validas), 2)

    return render(request, 'plantaopro/pages/boletim.html', {
        'aluno': aluno,
        'boletim': dict(boletim)
    })


@csrf_exempt
@login_required
@transaction.atomic
def cadastrar_disciplina(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            nome = data.get('nome', '').strip()

            if not nome:
                return JsonResponse({'success': False, 'error': 'Nome da disciplina é obrigatório.'}, status=400)

            escola = request.user.escola
            if not escola:
                return JsonResponse({'success': False, 'error': 'Usuário sem escola vinculada.'}, status=400)

            # Verifica se já existe disciplina com o mesmo nome para essa escola
            if Disciplina.objects.filter(nome__iexact=nome, escola=escola).exists():
                return JsonResponse({'success': False, 'error': 'Essa disciplina já está cadastrada.'}, status=400)

            Disciplina.objects.create(nome=nome, escola=escola)

            return JsonResponse({'success': True, 'mensagem': 'Disciplina cadastrada com sucesso.'})
        except Exception as e:
            return JsonResponse({'success': False, 'error': f'Erro interno: {str(e)}'}, status=500)

    return JsonResponse({'success': False, 'error': 'Método não permitido.'}, status=405)


def pagina_cadastrar_disciplina(request):
    return render(
        request,
        'plantaopro/pages/cadastrar_disciplinas.html'
    )

@login_required
def usuario_sem_escola(request):
    return render(request, 'plantaopro/pages/erro_sem_escola.html')

@login_required
def visualizar_escola(request):
    escola = request.user.escola
    estados = [
        'AC', 'AL', 'AP', 'AM', 'BA', 'CE', 'DF', 'ES', 'GO', 'MA',
        'MT', 'MS', 'MG', 'PA', 'PB', 'PR', 'PE', 'PI', 'RJ', 'RN',
        'RS', 'RO', 'RR', 'SC', 'SP', 'SE', 'TO'
    ]
    return render(request, 'plantaopro/pages/escola_detalhes.html', {
        'escola': escola,
        'estados': estados
    })

@csrf_exempt
@login_required
def editar_escola(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            escola = request.user.escola

            campos_permitidos = ['nome', 'telefone', 'email', 'endereco', 'numero', 'complemento',
                                 'bairro', 'cidade', 'estado', 'site', 'cep']

            for campo in campos_permitidos:
                if campo in data:
                    setattr(escola, campo, data[campo])

            escola.save()
            return JsonResponse({'success': True})
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)}, status=500)

    return JsonResponse({'success': False, 'error': 'Método não permitido'}, status=405)

@csrf_exempt
@transaction.atomic
def salvar_turma(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)

            nome = data.get('nome', '').strip()
            turno = data.get('turno', '').strip()
            ano = data.get('ano', '').strip()
            sala = data.get('sala', '').strip()
            descricao = data.get('descricao', '').strip()
            professor_id = data.get('professor_id')
            alunos_ids = data.get('alunos_ids', [])

            if not (nome and turno and ano and sala and professor_id):
                return JsonResponse({'success': False, 'error': 'Campos obrigatórios ausentes.'}, status=400)

            escola = request.user.escola

            turma = Turma.objects.create(
                nome=nome,
                turno=turno,
                ano=ano,
                sala=sala,
                descricao=descricao,
                escola=escola
            )

            # Vincula alunos à turma
            if alunos_ids:
                alunos = Aluno.objects.filter(id__in=alunos_ids, escola=escola)
                turma.alunos.set(alunos)

            # Vincula disciplinas do professor à turma
            professor = Docente.objects.get(id=professor_id, escola=escola)
            disciplinas = professor.disciplinas.all()

            for disciplina in disciplinas:
                TurmaDisciplina.objects.create(
                    turma=turma,
                    professor=professor,
                    disciplina=disciplina
                )

            return JsonResponse({'success': True, 'turma_id': turma.id})

        except Exception as e:
            transaction.set_rollback(True)
            return JsonResponse({'success': False, 'error': str(e)}, status=500)

    return JsonResponse({'success': False, 'error': 'Método inválido'}, status=405)

@csrf_exempt
def listar_disciplinas(request):
    disciplinas = Disciplina.objects.all().values('id', 'nome')
    return JsonResponse({'disciplinas': list(disciplinas)})

@csrf_exempt
def editar_disciplina(request):
    data = json.loads(request.body)
    try:
        disciplina = Disciplina.objects.get(id=data['id'])
        disciplina.nome = data['nome']
        disciplina.save()
        return JsonResponse({'success': True})
    except:
        return JsonResponse({'success': False})

@csrf_exempt
def excluir_disciplina(request):
    data = json.loads(request.body)
    try:
        Disciplina.objects.get(id=data['id']).delete()
        return JsonResponse({'success': True})
    except:
        return JsonResponse({'success': False})
    
def pagina_404_teste(request):
    return render(request, '404.html', status=404)