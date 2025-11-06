from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import RegisterForm
from django.contrib.auth.views import LoginView
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from urllib.parse import urlencode
from django.urls import reverse
from .forms import DisciplinaForm
from .models import Disciplina
from django.shortcuts import get_object_or_404
from django.http import HttpResponseForbidden
from django.views.decorators.http import require_http_methods
from django.views.decorators.cache import never_cache


def home(request):
    return render(request, 'home.html')


def register(request):
    """Register a new user and create either Aluno or Professor profile depending on role."""
    next_param = request.GET.get('next') or request.POST.get('next')

    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            role = form.cleaned_data.get('role')
            if role == 'aluno':
                from .models import Aluno
                matricula = form.cleaned_data.get('matricula')
                data_nascimento = form.cleaned_data.get('data_nascimento')
                turma = form.cleaned_data.get('turma')
                Aluno.objects.create(user=user, matricula=matricula, data_nascimento=data_nascimento, turma=turma)
            elif role == 'professor':
                from .models import Professor
                situacao = form.cleaned_data.get('situacao')
                Professor.objects.create(user=user, situacao=situacao)

            messages.success(request, 'Conta criada com sucesso. Faça login.')
            if next_param:
                qs = urlencode({'next': next_param})
                login_url = reverse('login')
                return redirect(f"{login_url}?{qs}")
            return redirect('login')
    else:
        form = RegisterForm()

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
    # Ensure the user has an Aluno profile
    aluno = getattr(request.user, 'aluno', None)
    if not aluno:
        messages.error(request, 'Você não tem perfil de aluno.')
        return redirect('home')

    turma = aluno.turma
    disciplinas = turma.disciplinas.all() if turma else []
    return render(request, 'aluno/principal_aluno.html', {'aluno': aluno, 'turma': turma, 'disciplinas': disciplinas})


@login_required
def principal_professor(request):
    # Ensure the user has a Professor profile
    professor = getattr(request.user, 'professor', None)
    if not professor:
        messages.error(request, 'Você não tem perfil de professor.')
        return redirect('home')

    disciplinas = professor.disciplinas.all()
    return render(request, 'professor/principal_professor.html', {'professor': professor, 'disciplinas': disciplinas})


@login_required
def add_disciplina(request):
    professor = getattr(request.user, 'professor', None)
    if not professor:
        messages.error(request, 'Você não tem perfil de professor.')
        return redirect('home')

    if request.method == 'POST':
        form = DisciplinaForm(request.POST)
        if form.is_valid():
            nome = form.cleaned_data['nome']
            turmas = form.cleaned_data.get('turmas')
            # create disciplina and assign professor
            disciplina, created = Disciplina.objects.get_or_create(
                nome=nome, defaults={'professor': professor}
            )
            if not created:
                # update professor if empty
                if disciplina.professor is None:
                    disciplina.professor = professor
                    disciplina.save()
            # Ensure disciplina is linked to all selected turmas
            if turmas:
                # use the reverse relation on Disciplina to set turmas in bulk
                disciplina.turmas.set(turmas)
            else:
                # if somehow empty (validation should prevent this), clear relations
                disciplina.turmas.clear()
            messages.success(request, f"Disciplina '{disciplina.nome}' registrada.")
            return redirect('principal_professor')
    else:
        form = DisciplinaForm()
    return render(request, 'professor/add_disciplina.html', {'form': form})


@login_required
def edit_disciplina(request, pk):
    professor = getattr(request.user, 'professor', None)
    if not professor:
        messages.error(request, 'Você não tem perfil de professor.')
        return redirect('home')

    disciplina = get_object_or_404(Disciplina, pk=pk)

    # Only allow the professor who teaches this disciplina to edit it (or allow if no professor assigned)
    if disciplina.professor and disciplina.professor != professor:
        return HttpResponseForbidden('Você não tem permissão para editar esta disciplina.')

    if request.method == 'POST':
        form = DisciplinaForm(request.POST, instance=disciplina)
        if form.is_valid():
            disciplina = form.save(commit=False)
            # ensure professor is set if not already
            if disciplina.professor is None:
                disciplina.professor = professor
            disciplina.save()
            # set turmas according to selection
            turmas = form.cleaned_data.get('turmas')
            if turmas:
                disciplina.turmas.set(turmas)
            else:
                disciplina.turmas.clear()
            messages.success(request, f"Disciplina '{disciplina.nome}' atualizada.")
            return redirect('principal_professor')
    else:
        # Populate the form with the existing instance
        form = DisciplinaForm(instance=disciplina, initial={'turmas': disciplina.turmas.all()})

    return render(request, 'professor/edit_disciplina.html', {'form': form, 'disciplina': disciplina})


@login_required
@require_http_methods(["GET", "POST"])
def delete_disciplina(request, pk):
    professor = getattr(request.user, 'professor', None)
    if not professor:
        messages.error(request, 'Você não tem perfil de professor.')
        return redirect('home')

    disciplina = get_object_or_404(Disciplina, pk=pk)

    # Only the professor who owns the disciplina (or unassigned) may delete
    if disciplina.professor and disciplina.professor != professor:
        return HttpResponseForbidden('Você não tem permissão para excluir esta disciplina.')

    if request.method == 'POST':
        nome = disciplina.nome
        disciplina.delete()
        messages.success(request, f"Disciplina '{nome}' excluída com sucesso.")
        return redirect('principal_professor')

    # GET -> show confirmation
    return render(request, 'professor/confirm_delete_disciplina.html', {'disciplina': disciplina})


@login_required
@never_cache
def disciplina_detail(request, pk):
    """Show details for a discipline.

    - All authenticated users may view the disciplina name and professor.
    - If the logged-in user is the professor who teaches it, also show students grouped by turma.
    - If the logged-in user is an aluno, ensure the disciplina belongs to their turma.
    """
    disciplina = get_object_or_404(Disciplina, pk=pk)

    user = request.user
    is_professor_owner = False
    can_view_students = False

    if hasattr(user, 'professor') and disciplina.professor and disciplina.professor == user.professor:
        is_professor_owner = True
        can_view_students = True

    # If user is aluno, only allow if the disciplina is in their turma
    if hasattr(user, 'aluno'):
        aluno = user.aluno
        turma = aluno.turma
        if turma not in disciplina.turmas.all():
            messages.error(request, 'Você não tem acesso a esta disciplina.')
            return redirect('principal_aluno')

    # Build students_by_turma only if the professor owner requests it
    students_by_turma = None
    if can_view_students:
        students_by_turma = []
        for t in disciplina.turmas.all():
            alunos = list(t.alunos.select_related('user').all())
            students_by_turma.append((t, alunos))

    return render(request, 'disciplina/detail.html', {
        'disciplina': disciplina,
        'is_professor_owner': is_professor_owner,
        'students_by_turma': students_by_turma,
    })


def logout_view(request):
    logout(request)
    # informar o usuário e mostrar a página de logout
    messages.info(request, 'Você saiu com sucesso.')
    return render(request, 'autenticacao/logged_out.html')


@login_required
def dashboard(request):
    """Redirect user to their role-specific dashboard (aluno or professor)."""
    user = request.user
    # safe hasattr checks in Python code
    if hasattr(user, 'aluno'):
        return redirect('principal_aluno')
    if hasattr(user, 'professor'):
        return redirect('principal_professor')
    messages.error(request, 'Você não tem um painel associado.')
    return redirect('home')
