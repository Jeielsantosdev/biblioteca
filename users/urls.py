from django.urls import path
from . import views

urlpatterns = [
    path('cadastro/',views.cadastro, name='cadastro'),
    path('activate/<int:id>/', views.activate, name='activate'),
    path('login/', views.login_view,name="login"),
    path("logout/", views.user_logout, name="logout"),
    path('home/', views.home, name='home'),
    path('perfil/', views.perfil_view, name='perfil'),
    
]
