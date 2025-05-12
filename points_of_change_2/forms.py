from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

# Você pode tanto usar os forms aqui ou diretamente em views, pelo requery.id = xxxx; mas aqui fica bem mais organzido
class RegistroForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')

