from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path('', views.home, name='home'),

    # Authentication
    path('auth/login/', auth_views.LoginView.as_view(template_name='autenticacao/login.html'), name='login'),
    path('auth/logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('auth/cadastro/', views.register, name='register'),

    #Painel do aluno
    #path('aluno/dashboard/', views.dashboard_aluno, name='dashboard_aluno'),

    #Painel do professor
    #path('professor/dashboard/', views.dashboard_professor, name='dashboard_professor'),
    #path('professor/lancar/<int:turma_id>/<int:disciplina_id>/',views.lancar_notas, name='lancar_notas'),
]