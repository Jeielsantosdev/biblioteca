from django.urls import path
from . import views

urlpatterns = [
    path('cadastro/',views.cadastro, name='cadastro'),
    path('activate/<int:id>/', views.activate, name='activate')
    
]
