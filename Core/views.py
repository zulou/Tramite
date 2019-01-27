from django.shortcuts import render
from django.contrib.auth.decorators import login_required

# Create your views here.

@login_required(redirect_field_name='my_redirect_field')
def base(request):
    return render(request, 'base.html')

def index(request):
    data = {}
    data['home'] = 'active'
    return render(request, 'index.html', {'menu': data, })

def login(request):
    return render(request, 'registration/login.html')

def dashboard_mesa_partes(request):
    return render(request, 'dmp/expedientes.html')
def dashboard_users(request):
    return render(request, 'dusers/expedientes.html')