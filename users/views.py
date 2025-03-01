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
import re




def validate_password(password):
    if len(password) != 8:
        raise ValidationError("A senha deve ter exatamente 8 caracteres.")

    if not re.search(r'[A-Za-z]', password):  # Verifica se tem pelo menos uma letra
        raise ValidationError("A senha deve conter pelo menos uma letra.")

    if not re.search(r'\d', password):  # Verifica se tem pelo menos um número
        raise ValidationError("A senha deve conter pelo menos um número.")

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
        try:
            validate_password(senha)
        except ValidationError as e:
            messages.error(request, str(e))  # Exibir mensagem de erro para o usuário
            return redirect('cadastro')

        cadastro = Cadastro(username=username,user_email=user_email,date_birth=date_birth,senha=make_password(senha),foto=foto, is_active=False)
        
        cadastro.save()

        activation = request.build_absolute_uri(reverse("activate", kwargs={"id": cadastro.id}))
       

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
    if request.method == "GET":
        cadastro = Cadastro.objects.all()
    return render(request, "home.html", {'cadastro':cadastro})
@login_required
def perfil_view(request):
    

    return render(request, 'perfil.html', )

def delete_view(request, id):
    if not request.user.is_authenticated:
        messages.error(request, "Você precisa estar logado para deletar sua conta.")
        return redirect('login')

    if request.user.id != id:
        messages.error(request, "Você não tem permissão para deletar esta conta.")
        return redirect('perfil')

    usuario = get_object_or_404(Cadastro, id=id)
    usuario.delete()
    
    logout(request)  # Desloga o usuário após deletar a conta
    messages.success(request, "Conta deletada com sucesso.")
    return redirect('login')

def update_view(request):
    if not request.user.is_authenticated:
        messages.error(request,"Voçê precisa fazer login")
        return redirect('login')
    users = get_object_or_404(Cadastro,id=request.user.id)

    if request.method == "POST":
        username = request.POST.get('username', '').strip()
        user_email = request.POST.get('user_email', '').strip()
        senha = request.POST.get('senha', '').strip()
        foto = request.FILES.get('foto')

        if not username or not user_email:
            messages.error(request,"O nome e o email não podem está vazios")
            return redirect('update')
        
        email_autrld = users.user_email != user_email

        users.username = username
        users.user_email = user_email

        if senha:
            users.set_password(senha)
        if foto:
            users.foto = foto
        users.save()
        
        if email_autrld: 
            activation = request.build_absolute_uri(reverse("activate", kwargs={"id": cadastro.id}))
       

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
            messages.success(request,"Conta atualizada! Verifique seu novo email para ativação.")
        else:
            messages.success(request,"Conta atualizada com sucesso!")
        return redirect('perfil')
    return render(request,'update.html', {'users':users})
