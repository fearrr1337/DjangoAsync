from django.shortcuts import render, redirect
from django.contrib.auth import login
from .forms import CustomUserCreationForm
from .decorators import role_required
from django.contrib.auth.decorators import login_required
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Article
from .forms import ArticleForm
from .policies import ArticlePolicy
from .mixins import PolicyMixin
from django.http import JsonResponse
from .tasks import add, send_welcome_email  # <-- новый импорт

def test(request):
    task = add.delay(2, 3)
    return JsonResponse({"task_id": task.id})

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

def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            # Асинхронная отправка приветственного письма
            send_welcome_email.delay(user.id)
            login(request, user)
            return redirect('home')
    else:
        form = CustomUserCreationForm()
    return render(request, 'core/register.html', {'form': form})

class ArticleListView(LoginRequiredMixin, ListView):
    model = Article
    template_name = "articles/list.html"

class ArticleDetailView(LoginRequiredMixin, DetailView):
    model = Article
    template_name = "articles/detail.html"

class ArticleCreateView(LoginRequiredMixin, CreateView):
    model = Article
    form_class = ArticleForm
    template_name = "articles/create.html"
    success_url = reverse_lazy("article_list")

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

class ArticleUpdateView(LoginRequiredMixin, PolicyMixin, UpdateView):
    model = Article
    form_class = ArticleForm
    template_name = "articles/update.html"
    success_url = reverse_lazy("article_list")
    policy_class = ArticlePolicy
    policy_action = "can_edit"

class ArticleDeleteView(LoginRequiredMixin, PolicyMixin, DeleteView):
    model = Article
    template_name = "articles/delete.html"
    success_url = reverse_lazy("article_list")
    policy_class = ArticlePolicy
    policy_action = "can_delete"