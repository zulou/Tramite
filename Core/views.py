from django.shortcuts import render

# Create your views here.
def index(request):
    data = {}
    data['home'] = 'active'
    return render(request, 'index.html', {'menu': data, })