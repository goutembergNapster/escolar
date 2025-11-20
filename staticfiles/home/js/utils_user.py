from django.contrib.auth import get_user_model

User = get_user_model()

def criar_usuario_com_cpf(cpf, senha, role, escola=None, email=None, is_staff=False, is_superuser=False):
    # Verifica se já existe um usuário com esse CPF
    if User.objects.filter(cpf=cpf).exists():
        return User.objects.get(cpf=cpf)

    # Cria o usuário com CPF também como username
    user = User.objects.create_user(
        username=cpf,
        cpf=cpf,
        password=senha,
        email=email or '',
        role=role,
        escola=escola
    )

    user.is_active = True
    user.is_staff = is_staff  # False por padrão, evita acesso ao admin
    user.is_superuser = is_superuser
    user.save()

    return user