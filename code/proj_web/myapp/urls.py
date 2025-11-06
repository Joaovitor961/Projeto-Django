from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),

    #Painel do aluno
    #path('aluno/dashboard/', views.dashboard_aluno, name='dashboard_aluno'),

    #Painel do professor
    #path('professor/dashboard/', views.dashboard_professor, name='dashboard_professor'),
    #path('professor/lancar/<int:turma_id>/<int:disciplina_id>/',views.lancar_notas, name='lancar_notas'),
]