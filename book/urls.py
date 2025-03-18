from django.urls import path
from . import views
urlpatterns = [
    path('emprestimo/',views.emprestimo, name='emprestimo'),
    path('', views.home, name='home'),
    path('livro/<int:pk>/', views.livro, name='livro'),
]
