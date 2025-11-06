from django import setup
from pathlib import Path
import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE','proj_web.settings')
setup()

from django.contrib.auth.models import User
from myapp.models import Turma, Disciplina

# link turma id 1 with disciplina id 1 if both exist and not already linked
try:
    turma = Turma.objects.filter(id=1).first()
    disciplina = Disciplina.objects.filter(id=1).first()
    if turma and disciplina:
        if disciplina not in turma.disciplinas.all():
            turma.disciplinas.add(disciplina)
            print(f'Linked turma {turma} with disciplina {disciplina}')
        else:
            print('Already linked')
    else:
        print('turma or disciplina id=1 not found; no changes made')
except Exception as e:
    print('Error:', e)
