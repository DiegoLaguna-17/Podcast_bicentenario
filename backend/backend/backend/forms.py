# backend/forms.py
from django import forms
from .models import Usuario


class UsuarioForm(forms.ModelForm):
    contrasenia = forms.CharField(widget=forms.PasswordInput())
    
    class Meta:
        model = Usuario
        fields = ['usuario', 'contrasenia', 'correo', 'rol']


