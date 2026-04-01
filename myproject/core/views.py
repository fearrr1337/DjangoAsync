from django.shortcuts import render,redirect
# redirect - перенаправление на другую страницу
from django.contrib.auth.forms import UserCreationForm
# UserCreationForm - готовая встроенная форма Django для регистрации новых пользователей
from django.contrib import messages
# message - всплывающие сообщения

from django.contrib.auth import login
from .forms import CustomUserCreationForm
from .decorators import role_required
from django.contrib.auth.decorators import login_required



@login_required
@role_required(['moderator', 'admin'])
def moderator_page(request):
    return render(request, 'core/moderator_page.html')

@login_required
@role_required(['admin'])
def admin_page(request):
    return render(request, 'core/admin_page.html')

def home_view(request):
    return render(request, 'core/home.html')

# Create your views here.
def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('home')
    else:
        form = CustomUserCreationForm()
    return render(request, 'core/register.html', {'form': form})