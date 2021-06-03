from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User, auth
from .forms import loginForm
from django.contrib import messages

def signup(request):
    if request.method == 'POST':
        signupforum = UserCreationForm(request.POST)
        if signupforum.is_valid():
            signupforum.save()
            return redirect('login')

    else:
        signupforum = UserCreationForm()
    context= {
    'signup': signupforum


    }
    return render(request,'login\signup.html',context)


def login(request):
    if request.method == 'POST':
        Loginform = loginForm(request.POST)
        if Loginform.is_valid():
            name = Loginform.cleaned_data['Username']
            Password = Loginform.cleaned_data['Password']
            user = auth.authenticate(username=name,password=Password)
            if user is not None:
                auth.login(request,user)
                return redirect('/')
            else:
                messages.info(request,'invalid username or password')


    else:
        Loginform = loginForm()
    context= {
    'form':Loginform
    }
    return render(request,'login\login.html',context)

def logout(request):
    auth.logout(request)
    return redirect('/')    
