# usuarios/forms.py

from django import forms
from .models import Usuarios

class UsuariosForm(forms.ModelForm):
    contrasena = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = Usuarios
        fields = ['nombre', 'correo', 'edad','contrasena']

    def clean_edad(self):
        edad = self.cleaned_data['edad']
        if edad < 18:
            raise forms.ValidationError('La edad debe ser mayor o igual a 18.')
        return edad
    

class LoginForm(forms.Form):
    correo = forms.EmailField(label="Correo electrónico")
    contrasena = forms.CharField(label="Contraseña", widget=forms.PasswordInput)