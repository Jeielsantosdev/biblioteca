from django.shortcuts import render, redirect,get_list_or_404,get_object_or_404
from .models import Cadastro
from django.contrib import messages
from django.contrib.messages import constants
from django.http import HttpResponse,Http404
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.core.exceptions import ValidationError
from django.urls import reverse
from django.contrib.auth.hashers import make_password

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
        

        cadastro = Cadastro(username=username,user_email=user_email,date_birth=date_birth,senha=make_password(senha),foto=foto)
        cadastro.is_active = False
        cadastro.save()

        activation = request.build_absolute_uri(f"/activate/{cadastro.id}/")
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
        return redirect(f'/activate/{cadastro.id}/')
def activate(request, id):
    user = get_object_or_404(Cadastro,id=id)

    if user.is_active:

        return render(request,'activate.html', {'username':user.username,'already_active':True })
    user.is_active = True
    user.save()
    
    return render(request, 'activate.html', {'username': user.username, 'already_active': False})