from django.urls import path
from . import views
urlpatterns = [
    path('livro/', views.livro, name='livro'),
    path('emprestimo/',views.emprestimo, name='emprestimo')
]
