from django import forms
from .models import Proyecto, Tarea
from usuarios.models import UserProfile

class ProyectoForm(forms.ModelForm):
    colaboradores = forms.ModelMultipleChoiceField(
        queryset=UserProfile.objects.filter(role__in=['GESTOR', 'COLAB']),
        widget=forms.CheckboxSelectMultiple,
        required=False
    )

    class Meta:
        model = Proyecto
        fields = ['nombre', 'descripcion', 'estado', 'fecha_inicio', 'fecha_limite', 'colaboradores']
        widgets = {
            'fecha_inicio': forms.DateInput(attrs={'type': 'date'}),
            'fecha_limite': forms.DateInput(attrs={'type': 'date'}),
            'descripcion': forms.Textarea(attrs={'rows': 3}),
        }

class TareaForm(forms.ModelForm):
    asignados = forms.ModelMultipleChoiceField(
        queryset=UserProfile.objects.filter(role='COLAB'),
        widget=forms.CheckboxSelectMultiple,
        required=False
    )

    class Meta:
        model = Tarea
        fields = ['titulo', 'descripcion', 'estado', 'fecha_limite', 'asignados']
        widgets = {
            'fecha_limite': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
            'descripcion': forms.Textarea(attrs={'rows': 3}),
        }