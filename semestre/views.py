from django.shortcuts import render

# Create your views here.
from django.shortcuts import render, redirect, get_object_or_404
from .models import Semestre
from .forms import SemestreForm

# Vista para listar los semestres
def listar_semestres(request):
    semestres = Semestre.objects.all()
    return render(request, 'semestres/listar_semestres.html', {'semestres': semestres})

# Vista para agregar un nuevo semestre
def agregar_semestre(request):
    if request.method == 'POST':
        form = SemestreForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('listar_semestres')  # Redirige a la lista de semestres
    else:
        form = SemestreForm()
    return render(request, 'semestres/agregar_semestre.html', {'form': form})

# Vista para editar un semestre existente
def editar_semestre(request, semestre_id):
    semestre = get_object_or_404(Semestre, id=semestre_id)
    if request.method == 'POST':
        form = SemestreForm(request.POST, instance=semestre)
        if form.is_valid():
            form.save()
            return redirect('listar_semestres')
    else:
        form = SemestreForm(instance=semestre)
    return render(request, 'semestres/editar_semestre.html', {'form': form, 'semestre': semestre})
