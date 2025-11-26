from django.urls import path
from . import views

urlpatterns = [

    # --------------------------------
    # Dashboard / Index
    # --------------------------------
    path('', views.index, name='index'),

    # --------------------------------
    # Escola
    # --------------------------------
    path('minha_escola/', views.visualizar_escola, name='minha_escola'),
    path('editar_escola/', views.editar_escola, name='editar_escola'),

    # --------------------------------
    # Professor
    # --------------------------------
    path('cadastro_professor/', views.cadastro_professor, name='cadastro_professor'),
    path('cadastrar_professor_banco/', views.cadastrar_professor_banco, name='cadastrar_professor_banco'),
    path('listar_professores/', views.listar_professores, name='listar_professores'),
    path('editar_professor/<int:prof_id>/', views.editar_professor, name='editar_professor'),
    path('alternar_status_professor/<int:prof_id>/', views.alternar_status_professor, name='alternar_status_professor'),

    # --------------------------------
    # Aluno
    # --------------------------------
    path('cadastro_aluno/', views.cadastrar_aluno, name='cadastro_aluno'),
    path('salvar_aluno/', views.salvar_aluno, name='salvar_aluno'),
    path('editar_aluno/<int:aluno_id>/', views.editar_aluno, name='editar_aluno'),
    path('alternar_status_aluno/<int:aluno_id>/', views.alternar_status_aluno, name='alternar_status_aluno'),
    path('listar_aluno/', views.listar_alunos, name='listar_aluno'),

    # PDFs do aluno
    path("alunos/<int:pk>/pdf/", views.aluno_requerimento_pdf, name="aluno_requerimento"),
    path('aluno/reimprimir/', views.reimprimir_documentos_aluno, name='reimprimir_documentos_aluno'),
    path("alunos/<int:pk>/comprovante/", views.comprovante_matricula_pdf, name="comprovante_matricula_pdf"),
    path("aluno/ficha/<int:pk>/", views.ficha_cadastral_pdf, name="ficha_cadastral_pdf"),

    # --------------------------------
    # Turma
    # --------------------------------
    path('turmas/', views.listar_turmas, name='listar_turmas'),
    path('turmas/<int:pk>/editar/', views.editar_turma, name='editar_turma'),
    path('turmas/<int:pk>/excluir/', views.excluir_turma, name='excluir_turma'),
    path('cadastro_turma/', views.cadastro_turma, name='cadastro_turma'),

    # ATENÇÃO: rota única para criação de turma
    path('criar_turma/', views.criar_turma, name='criar_turma'),  

    # --------------------------------
    # Funcionário
    # --------------------------------
    path('cadastro_funcionarios/', views.cadastro_funcionarios, name='cadastro_funcionarios'),
    path('cadastrar-funcionario/', views.cadastrar_funcionario_banco, name='cadastrar_funcionario_banco'),

    # --------------------------------
    # Buscar Pessoa
    # --------------------------------
    path('buscar_pessoa/', views.buscar_pessoa, name='buscar_pessoa'),
    path('autocomplete_pessoa/', views.autocomplete_pessoa, name='autocomplete_pessoa'),

    # --------------------------------
    # Impressão / Relatórios
    # --------------------------------
    path('imprimir_relatorios/', views.impressao_dados, name='imprimir_relatorios'),

    # --------------------------------
    # Notas / Boletim
    # --------------------------------
    path('registrar_notas/', views.registrar_notas, name='registrar_notas'),
    path('lancar_notas/', views.lancar_notas, name='lancar_notas'),

    path('boletins/', views.listar_turmas_para_boletim, name='listar_turmas_boletim'),
    path('boletins/<int:aluno_id>/', views.visualizar_boletim, name='visualizar_boletim'),

    # --------------------------------
    # Disciplinas
    # --------------------------------
    path('disciplinas/cadastrar/', views.cadastrar_disciplina, name='cadastrar_disciplina'),
    path('disciplinas/', views.pagina_cadastrar_disciplina, name='pagina_cadastrar_disciplina'),
    path('disciplinas/listar/', views.listar_disciplinas, name='listar_disciplinas'),
    path('disciplinas/editar/', views.editar_disciplina, name='editar_disciplina'),
    path('disciplinas/excluir/', views.excluir_disciplina, name='excluir_disciplina'),

    # --------------------------------
    # Usuário sem escola
    # --------------------------------
    path('erro/sem-escola/', views.usuario_sem_escola, name='usuario_sem_escola'),

    # --------------------------------
    # Chamada / Diário de Classe
    # --------------------------------
    path('diario-classe/', views.diario_classe, name='diario_classe'),
    path('salvar-chamada/', views.salvar_chamada, name='salvar_chamada'),
    path('buscar-alunos/<int:turma_id>/', views.buscar_alunos, name='buscar_alunos'),
    path('diario-classe/visualizar/', views.visualizar_chamada, name='visualizar_chamada'),
    path('diario-classe/editar-registro/<int:registro_id>/', views.editar_registro, name='editar_registro'),

    # --------------------------------
    # Login / Logout
    # --------------------------------
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),

    # --------------------------------
    # Troca de senha / Primeiro acesso
    # --------------------------------
    path('trocar_senha/', views.verificar_senha_temporaria, name='trocar_senha'),
    path('trocar_senha_api/', views.trocar_senha_api, name='trocar_senha_api'),

    # --------------------------------
    # Importar dados
    # --------------------------------
    path('importar_alunos/', views.importar_alunos, name='importar_alunos'),

    # --------------------------------
    # Admin temporário
    # --------------------------------
    path("criar-admin-temp/", views.create_admin_temp, name='criar-admin-temp'),

    # Nome da Turma (novo)
    path("turmas/nome/", views.pagina_nome_turma, name="pagina_nome_turma"),
    path("turmas/nome/cadastrar/", views.cadastrar_nome_turma, name="cadastrar_nome_turma"),
    path("turmas/nome/listar/", views.listar_nomes_turma, name="listar_nomes_turma"),
    path("turmas/nome/editar/", views.editar_nome_turma, name="editar_nome_turma"),
    path("turmas/nome/excluir/", views.excluir_nome_turma, name="excluir_nome_turma"),
]
