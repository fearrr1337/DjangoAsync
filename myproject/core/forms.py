from django.contrib.auth.forms import UserCreationForm, PasswordResetForm
from .models import CustomUser, Article
from django import forms
from .tasks import send_password_reset_email
from django.contrib.auth import get_user_model

User = get_user_model()

class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ('username', 'email', 'role', 'phone', 'birth_date', 'password1', 'password2')

class ArticleForm(forms.ModelForm):
    class Meta:
        model = Article
        fields = ["title", "content"]

class CustomPasswordResetForm(PasswordResetForm):
    def send_mail(self, subject_template_name, email_template_name,
                  context, from_email, to_email, html_email_template_name=None):
        user = context.get('user')
        if not user:
            return

        uid = context.get('uid')
        token = context.get('token')
        reset_url = f"{context['protocol']}://{context['domain']}/reset/{uid}/{token}/"

        from .tasks import send_password_reset_email
        send_password_reset_email.delay(user.id, reset_url)