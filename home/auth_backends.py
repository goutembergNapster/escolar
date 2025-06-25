from django.contrib.auth.backends import ModelBackend
from django.contrib.auth import get_user_model

UserModel = get_user_model()

class CPFBackend(ModelBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        try:
            # tenta autenticar por CPF
            user = UserModel.objects.get(cpf=username)
        except UserModel.DoesNotExist:
            try:
                # fallback para username (exigido pelo Django Admin)
                user = UserModel.objects.get(username=username)
            except UserModel.DoesNotExist:
                return None

        if user.check_password(password) and self.user_can_authenticate(user):
            return user
        return None

