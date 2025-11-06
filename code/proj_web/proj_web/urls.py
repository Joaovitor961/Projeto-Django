from django.contrib import admin
from django.urls import path, include
from myapp import views

urlpatterns = [
    path('', include('myapp.urls')),
    path('admin/', admin.site.urls),
]
