from django.shortcuts import render
from django.http import HttpResponse
from app.forms import *
# Create your views here.
def profil_data(request):
    dt=userform()
    dv=profilform()
    d={'dt':dt,'dv':dv}
    if request.method=='POST':
        ba=userform(request.POST)
        bb=profilform(request.POST)
        if ba.is_valid() and bb.is_valid():
            ba.save()
            bb.save()
            return HttpResponse('yes data inserte')
    return render(request,'profil_data.html',d)