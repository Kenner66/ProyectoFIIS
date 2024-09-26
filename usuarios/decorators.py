from django.shortcuts import redirect
from django.core.exceptions import PermissionDenied

def role_required(role):
    def decorator(view_func):
        def _wrapped_view(request, *args, **kwargs):
            if request.user.is_authenticated and (request.user.rol.nombre_rol == role or request.user.rol.is_admin):
                return view_func(request, *args, **kwargs)
            else:
                raise PermissionDenied  # Lanza un error si no tiene el rol correcto
        return _wrapped_view
    return decorator

