from django.contrib import admin
from django.urls import path, include
from myapp import views

urlpatterns = [
    path('', include('myapp.urls')),
    path('admin/', admin.site.urls),
    path('accounts/', include('django.contrib.auth.urls')),  # permite /accounts/login/
    path('testeparametros/', views.testeparametros, name='testeparametros')
]
