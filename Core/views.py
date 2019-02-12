from django.shortcuts import render, HttpResponse
from django.http import JsonResponse
from django.core import serializers
from django.views.decorators.csrf import csrf_protect, csrf_exempt
from django.core.files.storage import FileSystemStorage
from django.contrib.auth.decorators import login_required
from Core import models

import json,os


# Create your views here.



@login_required(redirect_field_name='my_redirect_field')
def index(request):
    data = {}
    data['home'] = 'active'
    return render(request, 'index.html', {'menu': data, })


def login(request):
    return render(request, 'registration/login.html')


@login_required(redirect_field_name='my_redirect_field')
def dashboard_mesa_partes(request):
    return render(request, 'dmp/dashboard.html')


def mesa_partes_expediente(request):
    return render(request, 'dmp/expedientes.html')


@login_required(redirect_field_name='my_redirect_field')
def dashboard_users(request):
    return render(request, 'dusers/dashboard.html')


@login_required(redirect_field_name='my_redirect_field')
def get_provincias(request, id):
    # data=models.Provincia.objects.value_list('id_departamento',flat=True)
    data = models.Provincia.objects.values('id', 'provincia').filter(id_departamento=id)
    return JsonResponse({'datos': list(data)})


@login_required(redirect_field_name='my_redirect_field')
def get_departamentos(request):
    data = models.Departamento.objects.values('id', 'departamento')
    return JsonResponse({'datos': list(data)})


@login_required(redirect_field_name='my_redirect_field')
def get_distritos(request, id):
    data = models.Distrito.objects.values('id', 'distrito').filter(id_provincia=id)
    return JsonResponse({'datos': list(data)})


@login_required(redirect_field_name='my_redirect_field')
def get_last_insert_person(request):
    latest_id = models.Person.objects.latest('id')
    return JsonResponse({'datos': {'id': latest_id.id, 'nombres': latest_id.per_name + " " + latest_id.per_lastname,
                                   'dni': latest_id.per_doc}})


@login_required(redirect_field_name='my_redirect_field')
def get_dni_autocomplete(request, dni):
    latest_id= models.Person.objects.values('id','per_doc','per_name','per_lastname').filter(per_doc__icontains=dni)
    return JsonResponse({'datos': list(latest_id)})

@login_required(redirect_field_name='my_redirect_field')
def get_person_dni(request, dni):
    latest_id= models.Person.objects.get(per_doc=dni)
    return JsonResponse({'datos': {'id': latest_id.id, 'nombres': latest_id.per_name + " " + latest_id.per_lastname,
                                   'dni': latest_id.per_doc}})
@login_required(redirect_field_name='my_redirect_field')
def get_tupa_autocomplete(request, tupa):
    latest_id= models.Tupa.objects.values('id','id_ofi_end','tup_des').filter(tup_des__icontains=tupa)
    return JsonResponse({'datos': list(latest_id)})

@login_required(redirect_field_name='my_redirect_field')
def get_last_document(request):
    latest_id= models.Document.objects.latest('id')
    return JsonResponse({'datos': {'id':latest_id.id}})

def get_last_document_movement(request):
    latest_id= models.Document.objects.latest('id')
    id_tup=models.Document.objects.values('id','id_tupa','id_type_document').filter(id=latest_id.id)
    #tupa = models.Tupa.objects.filter(id=latest_id.id)
    obj_attachment=models.Attachments(id_doc=latest_id,att_path=latest_id.id)
    obj_attachment.save()
    datos_tupa=models.Tupa.objects.filter(id=id_tup[0]['id_tupa']).values('id','id_ofi_begin','id_ofi_end')
    obj=models.Movements(mov_order=0,id_doc=latest_id,id_attachments=latest_id.id,id_ofi_begin=datos_tupa[0]['id_ofi_begin'],id_ofi_end=datos_tupa[0]['id_ofi_end'],id_doc_sender=id_tup[0]['id_tupa'],move_recibed=1)
    obj.save()
    return JsonResponse({'datos_document': list(id_tup), 'datos_tupa': list(datos_tupa)})



#@csrf_exempt
@login_required(redirect_field_name='my_redirect_field')
def register_attachment(request):
    if request.method == 'POST':
        if request.is_ajax():
            #form = FileUploadForm(data=request.POST, files=request.FILES)

            Diccionario = dict(request.POST.lists())
            path = Diccionario['path'][0]
            file =request.FILES['file']
            fs = FileSystemStorage(location=os.path.join('media/documents'))
            #fs = FileSystemStorage()
            filename = fs.save(str(path+".pdf"), file)
    return HttpResponse("Success")

@login_required(redirect_field_name='my_redirect_field')
def enviadosMp(request):
    documentos = models.Document.objects.all()
    data = {'documentos':documentos}
    return render(request, 'dmp/enviados.html', data)
