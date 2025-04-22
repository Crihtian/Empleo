from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.shortcuts import render, get_object_or_404, redirect
from .models import Proyecto, Tarea
from .forms import ProyectoForm, TareaForm

@login_required
def listar_proyectos(request):
    proyectos = Proyecto.objects.filter(colaboradores=request.user)
    return render(request, 'proyectos/listar_proyectos.html', {'proyectos': proyectos})

@login_required
def crear_proyecto(request):
    if not request.user.es_gestor:
        raise PermissionDenied
    
    if request.method == 'POST':
        form = ProyectoForm(request.POST)
        if form.is_valid():
            proyecto = form.save(commit=False)
            proyecto.save()
            proyecto.colaboradores.add(request.user)
            return redirect('detalle_proyecto', proyecto.id)
    else:
        form = ProyectoForm()
    return render(request, 'proyectos/form_proyecto.html', {'form': form})

@login_required
def detalle_proyecto(request, proyecto_id):
    proyecto = get_object_or_404(Proyecto.objects.prefetch_related('tareas'), id=proyecto_id)
    if request.user not in proyecto.colaboradores.all():
        raise PermissionDenied
    return render(request, 'proyectos/detalle_proyecto.html', {'proyecto': proyecto})

# Vistas similares para editar/eliminar proyectos y gestionar tareas