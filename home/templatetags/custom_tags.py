from django import template

register = template.Library()

@register.filter
def has_role(user, roles):
    """
    Verifica se o papel do usuário está dentro da lista de roles ou se é superusuário.
    Uso: {% if user|has_role:"diretor,coordenador" %}
    """
    if getattr(user, 'is_superuser', False):
        return True
    if not hasattr(user, 'role'):
        return False
    return user.role in [r.strip() for r in roles.split(',')]


@register.filter
def get_item(dictionary, key):
    return dictionary.get(key)

