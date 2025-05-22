from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms
from .models import Recomendacao

# Você pode tanto usar os forms aqui ou diretamente em views, pelo requery.id = xxxx; mas aqui fica bem mais organzido
class RegistroForm(UserCreationForm):
    email = forms.EmailField(required=True)
    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')

class RecomendacaoForm(forms.ModelForm):
    class Meta:
        model = Recomendacao
        fields = ['titulo', 'autor', 'data_publicacao', 'descricao',
                  'categoria', 'nome_postador', 'cargo_postador', 'arquivo']
        widgets = {
            'data_publicacao': forms.DateInput(attrs={'type': 'date'}),
        }

