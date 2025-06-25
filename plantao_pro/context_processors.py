def escola_no_contexto(request):
    return {
        'escola_vinculada': getattr(request.user, 'escola', None) if request.user.is_authenticated else None
    }
