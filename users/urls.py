from django.urls import path
from . import views

urlpatterns = [
    path('cadastro/',views.cadastro, name='cadastro'),
    path('activate/<int:id>/', views.activate, name='activate'),
    path('login/', views.login,name="login"),
    path("logout/", views.logout, name="logout"),
    path('home/', views.home, name='home'),
    
]
