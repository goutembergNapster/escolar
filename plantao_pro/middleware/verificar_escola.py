import logging
from django.shortcuts import redirect
from django.conf import settings

logger = logging.getLogger(__name__)

EXCEPT_URLS = [
    '/login/',
    '/logout/',
    '/erro/sem-escola/',
    '/admin/',
    '/admin/login/',
    '/static/',  
    '/aluno/',
]

class VerificaEscolaMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        path = request.path

        # Ignora URLs públicas ou arquivos estáticos
        if any(path.startswith(url) for url in EXCEPT_URLS):
            return self.get_response(request)

        user = request.user

        if user.is_authenticated:
            logger.debug(f"[MIDDLEWARE] Usuário autenticado: {user.username}")
            logger.debug(f"[MIDDLEWARE] Superusuário? {user.is_superuser}")
            logger.debug(f"[MIDDLEWARE] Caminho da requisição: {path}")

            # Permite que superusuário acesse qualquer rota
            if user.is_superuser:
                return self.get_response(request)

            # Verifica se tem escola associada
            if not hasattr(user, 'escola') or user.escola is None:
                logger.debug("[MIDDLEWARE] Redirecionando usuário sem escola")
                return redirect('usuario_sem_escola')

        return self.get_response(request)





