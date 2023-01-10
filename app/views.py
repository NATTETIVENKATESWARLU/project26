from django.shortcuts import render
from django.http import HttpResponse,HttpResponseRedirect
from django.contrib.auth import login,authenticate,logout
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from app.forms import *
from app.models import *
from django.core.mail import send_mail

# Create your views here.
def home(request):
    if request.session.get('username'):
        username=request.session.get('username')
        d={'username':username}
        return render(request,'home.html',d)
    return render(request,'home.html')



def profil_data(request):
    dt=userform()
    dv=profilform()
    d={'dt':dt,'dv':dv}
    if request.method=='POST' and request.FILES:
        ba=userform(request.POST)
        bb=profilform(request.POST,request.FILES)
        if ba.is_valid() and bb.is_valid():
            ma=ba.cleaned_data['password']
            uso=ba.save(commit=False)
            uso.set_password(ma)
            uso.save()


            na=bb.save(commit=False)
            na.user=uso
            na.save()
            send_mail('user registration',
                'regisrtatio successfuly',
                'n.venkateswarlu180@gmail.com',
                [uso.email],
                fail_silently=False)


            return HttpResponse('yes data inserte')
    return render(request,'profil_data.html',d)


def user_login(request):
    if request.method=='POST':
        username=request.POST['username']
        password=request.POST['password']
        user=authenticate(username=username,password=password)
        if user and user.is_active:
            login(request,user)
            request.session['username']=username
            return HttpResponseRedirect(reverse('home'))
    return render(request,'user_login.html')





@login_required
def user_logout(request):
    logout(request)
    return HttpResponseRedirect(reverse('home'))



@login_required
def profile_info(request):
    username=request.session.get('username')
    USD=User.objects.get(username=username)
    PFD=profile.objects.get(user=USD)
    d={'USD':USD,'PFD':PFD}
    return render(request,'profile_info.html',d)


@login_required
def chenge_password(request):
    if request.method=='POST':
        password=request.POST['password']
        username=request.session.get('username')
        USD=User.objects.get(username=username)
        USD.set_password(password)
        USD.save()
        send_mail('user registration',
            ' chenge_password successfuly',
            'n.venkateswarlu180@gmail.com',
            [USD[0].email],
            fail_silently=False)
        return HttpResponseRedirect(reverse('user_login'))
    return render(request,'chenge_password.html')



def forgot_password(request):
    if request.method=='POST':
        username=request.POST['username']
        password=request.POST['password']
        
        USD=User.objects.filter(username=username)
        if USD:
            USD[0].set_password(password)
            USD[0].save()
            send_mail('user registration',
                ' forgot_password successfuly',
                'n.venkateswarlu180@gmail.com',
                [USD[0].email],
                fail_silently=False)
            return HttpResponseRedirect(reverse('user_login'))
    return render(request,'forgot_password.html')