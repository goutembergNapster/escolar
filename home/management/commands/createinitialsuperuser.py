from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model

class Command(BaseCommand):
    help = "Cria o superusuário inicial automaticamente (se não existir)."

    def handle(self, *args, **kwargs):
        User = get_user_model()

        username = "goutemberg"
        email = "goutemberg@icloud.com"
        password = "Gps34587895@&*"

        if not User.objects.filter(username=username).exists():
            User.objects.create_superuser(username=username, email=email, password=password)
            self.stdout.write(self.style.SUCCESS("Superusuário criado com sucesso."))
        else:
            self.stdout.write(self.style.WARNING("Superusuário já existe. Ignorando."))
