from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import login, authenticate, logout

# Create your views here.
def userRegister(request):
    if request.method == 'POST':
        username =request.POST['kullanici']
        email = request.POST['email']
        sifre1 = request.POST['sifre1']
        sifre2 =request.POST['sifre2']

        if sifre1 == sifre2:
            if User.objects.filter(username = username).exists():
                messages.error(request, 'Kullanıcı Adı Kullanımda!')
            elif User.objects.filter(email = email).exists():
                messages.error(request, 'E mail Kullanı')
            elif len(sifre1) < 6:
                messages.error(request, 'Şifre  en az 6b karakter olmalı!')
            elif username.lower() in sifre1.lower():
                messages.error(request, 'Şifre ile kullanıcı adı benzer olmamalı')
            elif '.' not in sifre1:
                messages.error(request, 'Şifrede en az 1 tane (.) olmalıdır!')
            else:
                # kullanıcının kayıt olacağı kısım
                user = User.objects.create_user(
                    username = username,
                    email = email,
                    password =sifre1
                )
                user.save()
                messages.success(request, 'Kullanıcı OLluşturuldu')
                return redirect ('index')
        else:
            messages.error(request, 'Şifreler Uyuşmuyor!')    
    return render(request, 'user/register.html')

def userLogin(request):
    if request.method == 'POST':
        kullanici = request.POST['kullanici']
        sifre = request.POST['sifre']

        user = authenticate(request, username = kullanici, password = sifre)

        if user is not None:
            login(request, user)
            messages.success(request, 'Giriş Yapıldı')
            return redirect('index')
        else:
            messages.error(request, 'Kullanıcı adı veya şifre hatalı!')
    return render(request, 'user/login.html')

def userLogout(request):
    logout(request)
    messages.success(request, "Çıkış Yapıldı")
    return redirect('index')