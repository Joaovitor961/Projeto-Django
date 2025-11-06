from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.contrib.auth.views import LoginView
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from urllib.parse import urlencode
from django.urls import reverse


def home(request):
    return render(request, 'home.html')


def register(request):
    """Register a new user using Django's built-in UserCreationForm."""
    # preserve 'next' so after creating account user can be redirected to login with next
    next_param = request.GET.get('next') or request.POST.get('next')

    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Conta criada com sucesso. Faça login.')
            # redirect to login, preserving next if present
            if next_param:
                qs = urlencode({'next': next_param})
                login_url = reverse('login')
                return redirect(f"{login_url}?{qs}")
            return redirect('login')
    else:
        form = UserCreationForm()

    return render(request, 'autenticacao/register.html', {'form': form, 'next': next_param})


class CustomLoginView(LoginView):
    template_name = 'autenticacao/login.html'

    def get_success_url(self):
        user = self.request.user
        if hasattr(user, 'aluno'):
            return '/aluno/home/'
        elif hasattr(user, 'professor'):
            return '/professor/home/'
        else:
            return '/'


@login_required
def principal_aluno(request):
    return render(request, 'aluno/principal_aluno.html')


@login_required
def principal_professor(request):
    return render(request, 'professor/principal_professor.html')


def logout_view(request):
    logout(request)
    # informar o usuário e mostrar a página de logout
    messages.info(request, 'Você saiu com sucesso.')
    return render(request, 'autenticacao/logged_out.html')
