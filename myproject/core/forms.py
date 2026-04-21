from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser
from django import forms
from .models import Article

class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ('username', 'email', 'role', 'phone', 'birth_date', 'password1', 'password2')



class ArticleForm(forms.ModelForm):
    class Meta:
        model = Article
        fields = ["title", "content"]