from django.shortcuts import render,redirect
# redirect - перенаправление на другую страницу
from django.contrib.auth.forms import UserCreationForm
# UserCreationForm - готовая встроенная форма Django для регистрации новых пользователей
from django.contrib import messages
# message - всплывающие сообщения


def home_view(request):
    return render(request, 'core/home.html')

# Create your views here.
def register(request):
    if request.method == "POST": # если POST, мы обрабатываем данные

        form = UserCreationForm(request.POST) # берем стандартную форму Django и «наполняем» её данными, которые прислал пользователь

        if form.is_valid(): # проверяет пароли(совпадают ли, сложность), не занят ли username кем-то другим
            form.save() # Создает нового пользователя в базе данны

            messages.success(request, "Аккаунт успешно создан! Теперь войдите в систему.")

            return redirect('login')
    else: # если GET, то мы просто создаем пустую форму и показываем ее
        form = UserCreationForm()

    return render(request,"core/register.html", {'form': form})