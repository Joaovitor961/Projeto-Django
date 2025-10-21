from django.contrib import admin
from .models import Turma, Disciplina, Professor, Aluno

@admin.register(Turma)
class TurmaAdmin(admin.ModelAdmin):
    list_display = ('nome',)

@admin.register(Disciplina)
class DisciplinaAdmin(admin.ModelAdmin):
    list_display = ('nome',)

@admin.register(Professor)
class ProfessorAdmin(admin.ModelAdmin):
    list_display = ('user',)

@admin.register(Aluno)
class AlunoAdmin(admin.ModelAdmin):
    list_display = ('user', 'matricula', 'turma')
    search_fields = ('user__username', 'matricula')
