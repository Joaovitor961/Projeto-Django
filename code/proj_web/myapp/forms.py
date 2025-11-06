from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Turma, Disciplina


class RegisterForm(UserCreationForm):
    ROLE_CHOICES = (
        ('aluno', 'Aluno'),
        ('professor', 'Professor'),
    )

    role = forms.ChoiceField(choices=ROLE_CHOICES, widget=forms.RadioSelect, required=True)

    # Aluno fields
    matricula = forms.CharField(max_length=20, required=False)
    data_nascimento = forms.DateField(required=False, widget=forms.DateInput(attrs={'type': 'date'}))
    turma = forms.ModelChoiceField(queryset=Turma.objects.all(), required=False)

    # Professor fields
    situacao = forms.CharField(max_length=255, required=False)

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2')

    def clean(self):
        cleaned = super().clean()
        role = cleaned.get('role')
        if role == 'aluno':
            if not cleaned.get('matricula'):
                self.add_error('matricula', 'Matrícula é obrigatória para alunos.')
            if not cleaned.get('data_nascimento'):
                self.add_error('data_nascimento', 'Data de nascimento é obrigatória para alunos.')
            if not cleaned.get('turma'):
                self.add_error('turma', 'Turma é obrigatória para alunos.')
        elif role == 'professor':
            if not cleaned.get('situacao'):
                self.add_error('situacao', 'Situação é obrigatória para professores.')
        return cleaned


class DisciplinaForm(forms.ModelForm):
    # Use checkboxes so professors can clearly select multiple turmas
    turmas = forms.ModelMultipleChoiceField(
        queryset=Turma.objects.all(), required=True,
        widget=forms.CheckboxSelectMultiple
    )

    class Meta:
        model = Disciplina
        fields = ('nome',)

    def clean(self):
        cleaned = super().clean()
        turmas = cleaned.get('turmas')
        if not turmas or len(turmas) == 0:
            self.add_error('turmas', 'Selecione ao menos uma turma.')
        return cleaned
