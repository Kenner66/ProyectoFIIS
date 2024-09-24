from django.core.exceptions import PermissionDenied

from django.shortcuts import redirect

def role_required(role):
    def decorator(view_func):
        def _wrapped_view(request, *args, **kwargs):
            if request.user.is_authenticated and request.user.rol.nombre_rol == role:
                return view_func(request, *args, **kwargs)
            else:
                return redirect('home_estudiante')  # Redirige a la página de estudiante
        return _wrapped_view
    return decorator
