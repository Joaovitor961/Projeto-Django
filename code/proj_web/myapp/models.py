from django.db import models

class Turma(models.Model):
    nome = models.CharField(max_length=50, unique=True) 

class Disciplina(models.Model):
    nome = models.CharField(max_length=100, unique=True)

class Professor(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='professor')
    departamento = models.CharField(max_length=255)

class Aluno(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='aluno')
    #user = models.CharField(max_length=255)
    matricula = models.CharField(max_length=20, unique=True)
    data_nascimento = models.DateField()
    #turma = models.CharField(max_length=3)
    turma = models.ForeignKey(Turma, on_delete=models.PROTECT, related_name='alunos')