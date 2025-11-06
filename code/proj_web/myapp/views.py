from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.contrib.auth.views import LoginView
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout


def home(request):
    return render(request, 'home.html')


def register(request):
    """Register a new user using Django's built-in UserCreationForm."""
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Conta criada com sucesso. Faça login.')
            return redirect('login')
    else:
        form = UserCreationForm()
    return render(request, 'autenticacao/register.html', {'form': form})


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
    return redirect('home')
