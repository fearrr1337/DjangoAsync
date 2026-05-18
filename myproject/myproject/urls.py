from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views
from core import views as core_views
from core.forms import CustomPasswordResetForm

urlpatterns = [
    path('moderator/', core_views.moderator_page, name='moderator_page'),
    path('adminp/', core_views.admin_page, name='admin_page'),
    path('', core_views.home_view, name='home'),

    path('admin/', admin.site.urls),

    # статьи
    path('articles/', include('core.urls')),

    # регистрация
    path('register/', core_views.register, name='register'),

    # вход / выход
    path('login/', auth_views.LoginView.as_view(template_name='core/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),

    # сброс пароля (используем кастомную форму, которая отправляет письмо через Celery)
    path('password_reset/',
         auth_views.PasswordResetView.as_view(
             template_name='core/password_reset.html',
             form_class=CustomPasswordResetForm
         ),
         name='password_reset'),

    path('password_reset_done/',
         auth_views.PasswordResetDoneView.as_view(template_name='core/password_reset_done.html'),
         name='password_reset_done'),

    path('reset/<uidb64>/<token>/',
         auth_views.PasswordResetConfirmView.as_view(template_name='core/password_reset_confirm.html'),
         name='password_reset_confirm'),

    path('reset/done/',
         auth_views.PasswordResetCompleteView.as_view(template_name='core/password_reset_complete.html'),
         name='password_reset_complete'),
]