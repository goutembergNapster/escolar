from django.urls import path
from .views import login_view, logout_view  
from . import views
from .views import salvar_aluno, cadastrar_disciplina, pagina_cadastrar_disciplina, usuario_sem_escola
from .views import criar_turma, verificar_senha_temporaria, importar_alunos, trocar_senha_api, listar_turmas_para_boletim, visualizar_boletim

urlpatterns = [
    
    path('', views.index, name='index'),

    # Escola
    path('minha_escola/', views.visualizar_escola, name='minha_escola'),
    path('editar_escola/', views.editar_escola, name='editar_escola'),

    # Professor
    path('cadastro_professor/', views.cadastro_professor, name='cadastro_professor'),
    path('cadastrar_professor_banco/', views.cadastrar_professor_banco, name='cadastrar_professor_banco'),
    path('listar_professores/', views.listar_professores, name='listar_professores'),
    path('editar_professor/<int:prof_id>/', views.editar_professor, name='editar_professor'),
    path('alternar_status_professor/<int:prof_id>/', views.alternar_status_professor, name='alternar_status_professor'),

    # Aluno
    
    path('salvar_aluno/', salvar_aluno, name='salvar_aluno'),
    path('cadastro_aluno/', views.cadastrar_aluno, name='cadastro_aluno'),
    path('editar_aluno/<int:aluno_id>/', views.editar_aluno, name='editar_aluno'),
    path('alternar_status_aluno/<int:aluno_id>/', views.alternar_status_aluno, name='alternar_status_aluno'),
    path('listar_aluno/', views.listar_alunos, name='listar_aluno'),


    # Turma
    path('cadastro_turma/', views.cadastro_turma, name='cadastro_turma'),
    path('criar_turma/', criar_turma, name='criar_turma'),

    # Funcionário
    path('cadastro_funcionarios/', views.cadastro_funcionarios, name='cadastro_funcionarios'),
    path('cadastrar-funcionario/', views.cadastrar_funcionario_banco, name='cadastrar_funcionario_banco'),


    #Buscar Pessoa
    path('buscar_pessoa/', views.buscar_pessoa, name='buscar_pessoa'),
    path('autocomplete_pessoa/', views.autocomplete_pessoa, name='autocomplete_pessoa'),

   #Impressao
    
    path('imprimir_relatorios/', views.impressao_dados, name='imprimir_relatorios'),

    #Notas
    path('registrar_notas/', views.registrar_notas, name='registrar_notas'),
    path('lancar_notas/', views.lancar_notas, name='lancar_notas'),
    path('criar_turma/', views.salvar_turma, name='criar_turma'),

    #Login
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),

    #senha
    path('trocar_senha/', verificar_senha_temporaria, name='trocar_senha'),
    path('trocar_senha_api/', trocar_senha_api, name='trocar_senha_api'),

     #Importar dados
    path('importar_alunos/', importar_alunos , name='importar_alunos'),

    #Boletims
    path('boletins/', listar_turmas_para_boletim, name='listar_turmas_boletim'),
    path('boletins/<int:aluno_id>/', visualizar_boletim, name='visualizar_boletim'),

    #Disciplinas
    path('disciplinas/cadastrar/', cadastrar_disciplina, name='cadastrar_disciplina'),
    path('disciplinas/', pagina_cadastrar_disciplina, name='pagina_cadastrar_disciplina'),
    path('disciplinas/listar/', views.listar_disciplinas, name='listar_disciplinas'),
    path('disciplinas/editar/', views.editar_disciplina, name='editar_disciplina'),
    path('disciplinas/excluir/', views.excluir_disciplina, name='excluir_disciplina'),


    #usuario_sem_escola
    path('erro/sem-escola/', usuario_sem_escola, name='usuario_sem_escola'),


]