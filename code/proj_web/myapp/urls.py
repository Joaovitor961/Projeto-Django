from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),

    # Autenticação
    path('auth/login/', views.CustomLoginView.as_view(), name='login'),
    path('auth/logout/', views.logout_view, name='logout'),
    path('auth/cadastro/', views.register, name='register'),

    # Painel do aluno
    path('aluno/home/', views.principal_aluno, name='principal_aluno'),

    # Painel do professor
    path('professor/home/', views.principal_professor, name='principal_professor'),
    path('professor/disciplinas/add/', views.add_disciplina, name='add_disciplina'),
    path('professor/disciplinas/<int:pk>/edit/', views.edit_disciplina, name='edit_disciplina'),
    path('professor/disciplinas/<int:pk>/delete/', views.delete_disciplina, name='delete_disciplina'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('disciplinas/<int:pk>/', views.disciplina_detail, name='disciplina_detail'),
]
