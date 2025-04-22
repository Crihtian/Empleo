from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import UserProfile

class RegistroForm(UserCreationForm):
    role = forms.ChoiceField(
        choices=UserProfile.ROLES,
        label='Rol',
        help_text='Seleccione el tipo de usuario'
    )

    class Meta:
        model = UserProfile
        fields = ['username', 'first_name', 'last_name', 'email', 'role', 'password1', 'password2']
        labels = {
            'first_name': 'Nombre',
            'last_name': 'Apellidos'
        }

class UserUpdateForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['first_name', 'last_name', 'email', 'role']
        widgets = {
            'role': forms.Select(attrs={'disabled': 'disabled'})
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Solo admin puede cambiar roles
        if not self.instance.es_administrador:
            self.fields['role'].widget.attrs['disabled'] = True