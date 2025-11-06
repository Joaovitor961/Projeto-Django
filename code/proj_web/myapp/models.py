from django.db import models
from django.contrib.auth.models import User

class Turma(models.Model):
    nome = models.CharField(max_length=50, unique=True) 
    # Uma turma pode ter várias disciplinas e uma disciplina pode ser ministrada em várias turmas
    disciplinas = models.ManyToManyField('Disciplina', blank=True, related_name='turmas')

    def __str__(self):
        return self.nome

class Disciplina(models.Model):
    nome = models.CharField(max_length=100, unique=True)
    # Vincular disciplina a um professor (opcional)
    professor = models.ForeignKey('Professor', on_delete=models.SET_NULL, null=True, blank=True, related_name='disciplinas')

    def __str__(self):
        return self.nome

class Professor(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='professor')
    situacao = models.CharField(max_length=255)

    def __str__(self):
        # Mostra o nome de usuário do professor no Admin
        return self.user.username

class Aluno(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='aluno')
    #user = models.CharField(max_length=255)
    matricula = models.CharField(max_length=20, unique=True)
    data_nascimento = models.DateField()
    #turma = models.CharField(max_length=3)
    turma = models.ForeignKey(Turma, on_delete=models.PROTECT, related_name='alunos')

    def __str__(self):
        # Mostra o nome de usuário do aluno no Admin
        return self.user.username