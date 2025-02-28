from django.shortcuts import render, redirect,get_object_or_404
from .models import Cadastro
from django.contrib import messages
from django.utils.timezone import now
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.core.exceptions import ValidationError
from django.urls import reverse
from django.contrib.auth.hashers import make_password
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth.hashers import check_password
#from django.contrib.auth.models import user



# Função para validar a senha
def validate_password(password):
    if len(password) < 8:
        raise ValidationError("A senha deve ter pelo menos 6 caracteres.")
    if len(password) > 8:
        raise ValidationError("A senha não pode ter mais que 8 caracteres.")

def cadastro(request):

    if request.method == 'GET':
        cadastro = Cadastro.objects.all()
        print(cadastro)

        return render(request, 'cadastro.html', {'cadastro':cadastro})
    elif request.method == 'POST':
        

        username = request.POST.get('username')
        user_email = request.POST.get('user_email')
        date_birth = request.POST.get('date_birth')
        senha = request.POST.get('senha')
        foto = request.FILES.get('foto')
        #login(request, user)

        
        if len(username.strip()) == 0 or not foto:
            messages.error(request, 'Preencha todos os campos')
            return redirect('cadastro') 
        
        if Cadastro.objects.filter(user_email=user_email).exists():
            messages.error(request,'Erro: E-mail já cadastrado')
            return redirect('cadastro')
        

        cadastro = Cadastro(username=username,user_email=user_email,date_birth=date_birth,senha=make_password(senha),foto=foto, is_active=False)
        
        cadastro.save()

        activation = request.build_absolute_uri(reverse("activate", kwargs={"id": cadastro.id}))
        #0.0.0activation = request.build_absolute_uri(f'http:'{"id": cadastro.id})

        subject = "Ative sua conta"
        html_message = render_to_string("activate.html", {
        "username": cadastro.username,
        "activation": activation
        })
        send_mail(
            subject,
            f"Olá {cadastro.username}, clique no link para ativar sua conta: {activation}",
            "jeielsantos29@gmail.com",  # Endereço do remetente
            [user_email],  # Endereço do destinatário
            fail_silently=False,
            html_message=html_message
        )

       
        messages.success(request, 'Cadastro realizado! Verifique seu e-mail para ativação.')
        #return redirect(reverse("activate",kwargs={"id":cadastro.id}))
        return redirect('login')

def activate(request, id):
    user = get_object_or_404(Cadastro, id=id)

    if user.is_active:
        messages.info(request, f"A conta de {user.username} já está ativa.")
        return render(request, 'activate.html', {'username': user.username, 'already_active': True})
    
    user.is_active = True
    user.save()

    messages.success(request, f"A conta de {user.username} foi ativada com sucesso!")
    return redirect('login')  # Redireciona para o login

def login_view(request):
    if request.method == "POST":
        user_email = request.POST.get('user_email')
        senha = request.POST.get("senha")
        
        try:
            user = authenticate(request, user_email=user_email, senha=senha)
           
            
            if user is not None:  # Verifica a senha de forma segura
                if user.is_active:
                    user.last_login = now()
                    user.save()
                    
                    login(request, user)  # Realiza o login do usuário
                    print(f"Usuário autenticado: {request.user}")  # Verifique se o login foi bem-sucedido
                    
                    return redirect('home')  # Redireciona para a página 'home'
                else:
                    messages.error(request, "Sua conta está desativada, verifique seu email para ativá-la.")
            else:
                messages.error(request, "E-mail ou Senha incorretos.")
        
        except Cadastro.DoesNotExist:
            messages.error(request, "Usuário não encontrado.")
        
        return redirect('login')
    
    return render(request, 'login.html')

def user_logout(request):
    logout(request)
    messages.success(request, "Você saiu da sua conta!")
    return redirect("login")


@login_required
def home(request):
    return render(request, "home.html")

def perfil_view(request):

    return render(request, 'perfil.html')
    ...