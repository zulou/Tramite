from builtins import id

from django.forms import renderers
from django.shortcuts import render, HttpResponse
from django.http import JsonResponse
from django.utils.dateparse import parse_date

import datetime
import os.path
from django.db.models.query import QuerySet
from django.core import serializers
from django.views.decorators.csrf import csrf_protect, csrf_exempt
from django.core.files.storage import FileSystemStorage
from django.contrib.auth.decorators import login_required
from Core import models

import json, os


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


@login_required(redirect_field_name='my_redirect_field')
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
    latest_id = models.Person.objects.values('id', 'per_doc', 'per_name', 'per_lastname').filter(per_doc__icontains=dni)
    return JsonResponse({'datos': list(latest_id)})


@login_required(redirect_field_name='my_redirect_field')
def get_person_dni(request, dni):
    latest_id = models.Person.objects.get(per_doc=dni)
    return JsonResponse({'datos': {'id': latest_id.id, 'nombres': latest_id.per_name + " " + latest_id.per_lastname,
                                   'dni': latest_id.per_doc}})


@login_required(redirect_field_name='my_redirect_field')
def get_tupa_autocomplete(request, tupa):
    latest_id = models.Tupa.objects.values('id', 'id_ofi_end', 'tup_des').filter(tup_des__icontains=tupa)
    return JsonResponse({'datos': list(latest_id)})


@login_required(redirect_field_name='my_redirect_field')
def get_last_document(request):
    latest_id = models.Document.objects.latest('id')
    return JsonResponse({'datos': {'id': latest_id.id}})

@login_required(redirect_field_name='my_redirect_field')
def get_id_office(request,office,date):
    id_office = models.Office.objects.values('id').filter(ofi_des__icontains=office)
    #return(id_office[0])
    #today_min = datetime.datetime.combine(parse_date(date), datetime.time.min)
    #today_max = datetime.datetime.combine(parse_date(date), datetime.time.max)

    queryset = models.Office.objects.values('id', 'tupa_office_end__document_tupa__doc_number',
                                            'tupa_office_end__document_tupa__doc_exp_number',
                                            'tupa_office_end__document_tupa__doc_pages',
                                            'tupa_office_end__document_tupa__id_tupa'
                                            , 'tupa_office_end__document_tupa__id_person_id',
                                            'tupa_office_end__id_ofi_begin__id',
                                            'tupa_office_end__id_ofi_end__id',
                                            'tupa_office_end__document_tupa__doc_des',
                                            'tupa_office_end__document_tupa__id',
                                            'tupa_office_end__document_tupa__created').filter(pk=id_office[0]['id'])

    lista = []
    dic = {}
    #if not queryset:
    for entry in queryset:
        year = entry['tupa_office_end__document_tupa__created'].year
        print(year)
        month = entry['tupa_office_end__document_tupa__created'].month
        day = entry['tupa_office_end__document_tupa__created'].day

        date_year = parse_date(date).year
        date_month = parse_date(date).month
        date_day = parse_date(date).day

        if (int(day) == int(date_day)) and (int(month) == int(date_month)) and (int(year) == int(date_year)):

            id_tupa = models.Tupa.objects.values('tup_des').filter(pk=entry['tupa_office_end__document_tupa__id_tupa'])
            ofi_des_begin = models.Office.objects.values('ofi_des').filter(
                pk=entry['tupa_office_end__id_ofi_begin__id'])
            ofi_des_end = models.Office.objects.values('ofi_des').filter(pk=entry['tupa_office_end__id_ofi_end__id'])
            id_person = models.Person.objects.values('per_name', 'per_lastname').filter(
                pk=entry['tupa_office_end__document_tupa__id_person_id'])

            #dic['id'] = entry['tupa_office_end__document_tupa__id']
            dic['doc_number'] = entry['tupa_office_end__document_tupa__doc_number']
            dic['doc_exp_number'] = entry['tupa_office_end__document_tupa__doc_exp_number']
            dic['doc_pages'] = entry['tupa_office_end__document_tupa__doc_pages']
            dic['id_tupa'] = id_tupa[0]['tup_des']

            dic['id_person'] = str(id_person[0]['per_name'] + " " + id_person[0]['per_lastname'])
            dic['doc_begin'] = ofi_des_begin[0]['ofi_des']
            dic['doc_des'] = ofi_des_end[0]['ofi_des']
            dic['created'] = entry['tupa_office_end__document_tupa__created'].strftime('%m-%d-%Y')


            lista.append(dic.copy())

        else:
            #lista(lista);
            continue
            #return JsonResponse({'data': list(lista)})

    return JsonResponse({'data':list(lista)})




@login_required(redirect_field_name='my_redirect_field')
def get_last_document_movement(request):
    latest_id = models.Document.objects.latest('id')
    id_tup = models.Document.objects.values('id', 'id_tupa', 'id_type_document').filter(id=latest_id.id)
    # tupa = models.Tupa.objects.filter(id=latest_id.id)
    obj_attachment = models.Attachments(id_doc=latest_id, att_path=latest_id.id)
    obj_attachment.save()
    datos_tupa = models.Tupa.objects.filter(id=id_tup[0]['id_tupa']).values('id', 'id_ofi_begin', 'id_ofi_end')
    obj = models.Movements(mov_order=0, id_doc=latest_id, id_attachments=latest_id.id,
                           id_ofi_begin=datos_tupa[0]['id_ofi_begin'], id_ofi_end=datos_tupa[0]['id_ofi_end'],
                           id_doc_sender=id_tup[0]['id_tupa'], move_recibed=1)
    obj.save()
    return JsonResponse({'datos_document': list(id_tup), 'datos_tupa': list(datos_tupa)})


# @csrf_exempt
@login_required(redirect_field_name='my_redirect_field')
def register_attachment(request):
    if request.method == 'POST':
        if request.is_ajax():
            # form = FileUploadForm(data=request.POST, files=request.FILES)

            Diccionario = dict(request.POST.lists())
            if os.path.exists('media/documents/'+Diccionario['path'][0]+".pdf"):
                os.remove('media/documents/'+Diccionario['path'][0]+".pdf")

            path = Diccionario['path'][0]
            file = request.FILES['file']
            fs = FileSystemStorage(location=os.path.join('media/documents'))
            # fs = FileSystemStorage()
            filename = fs.save(str(path + ".pdf"), file)
    return HttpResponse("Success")


@login_required(redirect_field_name='my_redirect_field')
def enviadosMp(request):
    username = None
    if request.user.is_authenticated:
        username = request.user.username
        #pK_office = models.Office.objects.values('id').filter(ofi_des__icontains=username)
        queryset = models.Office.objects.values('id', 'tupa_office_begin__document_tupa__doc_number','tupa_office_begin__document_tupa__doc_exp_number','tupa_office_begin__document_tupa__doc_pages','tupa_office_begin__document_tupa__id_tupa','tupa_office_begin__document_tupa__id_person_id','tupa_office_begin__id_ofi_begin__id','tupa_office_begin__id_ofi_end__id','tupa_office_begin__document_tupa__doc_des','tupa_office_begin__document_tupa__id','tupa_office_begin__document_tupa__created').filter(ofi_des__icontains=username)

        #return HttpResponse(queryset)
        lista = []
        dic = {}

        for entry in queryset:

            try:
                ofi_des_begin = models.Office.objects.values('ofi_des').filter(pk=entry['tupa_office_begin__id_ofi_begin__id'])
                ofi_des_end = models.Office.objects.values('ofi_des').filter(pk=entry['tupa_office_begin__id_ofi_end__id'])
                id_person = models.Person.objects.values('per_name', 'per_lastname').filter(pk=entry['tupa_office_begin__document_tupa__id_person_id'])
                id_tupa = models.Tupa.objects.values('tup_des').filter(pk=entry['tupa_office_begin__document_tupa__id_tupa'])

                dic['id'] = entry['tupa_office_begin__document_tupa__id']
                dic['doc_number'] = entry['tupa_office_begin__document_tupa__doc_number']
                dic['doc_exp_number'] = entry['tupa_office_begin__document_tupa__doc_exp_number']
                dic['doc_pages'] = entry['tupa_office_begin__document_tupa__doc_pages']
                #return HttpResponse(entry['tupa_office_begin__document_tupa__id_tupa'])
                dic['id_tupa'] = id_tupa[0]['tup_des']
                dic['id_person'] = str(id_person[0]['per_name'] + " " + id_person[0]['per_lastname'])
                dic['doc_begin'] = ofi_des_begin[0]['ofi_des']
                dic['doc_des'] = ofi_des_end[0]['ofi_des']
                dic['created'] = entry['tupa_office_begin__document_tupa__created']
                lista.append(dic.copy())
            except:
                continue
        #return HttpResponse(pK_office)

        data = {'documentos': lista}
        return render(request, 'dmp/recibidos.html', data)
        #return HttpResponse(queryset)
    else:
        return HttpResponse("No esta logeado")


@login_required(redirect_field_name='my_redirect_field')
def related(request):
    id_tupa = models.Tupa.objects.get(pk=2)
    id_tupa.document_tupa.all()
    return HttpResponse(id_tupa.tup_des)


@login_required(redirect_field_name='my_redirect_field')
def comformidadMp(request):
    today_min = datetime.datetime.combine(datetime.date.today(), datetime.time.min)
    today_max = datetime.datetime.combine(datetime.date.today(), datetime.time.max)
    value_list = models.Document.objects.values_list('doc_des', flat=True).distinct().filter(
        created__range=(today_min, today_max))
    data = {'documentos': value_list, 'date': datetime.date.today().strftime('%Y-%m-%d')}
    return render(request, 'dmp/conformidad.html', data)

@login_required(redirect_field_name='my_redirect_field')
def get_documentos_conformidad(request,id,date):
    today_min = datetime.datetime.combine(parse_date(date), datetime.time.min)
    today_max = datetime.datetime.combine(parse_date(date), datetime.time.max)

    queryset = models.Office.objects.values('id', 'tupa_office_end__document_tupa__doc_number',
                                            'tupa_office_end__document_tupa__doc_exp_number',
                                            'tupa_office_end__document_tupa__doc_pages',
                                            'tupa_office_end__document_tupa__id_tupa'
                                            , 'tupa_office_end__document_tupa__id_person_id',
                                            'tupa_office_end__id_ofi_begin__id',
                                            'tupa_office_end__id_ofi_end__id',
                                            'tupa_office_end__document_tupa__doc_des',
                                            'tupa_office_end__document_tupa__id',
                                            'tupa_office_end__document_tupa__created').filter(pk=id)

    lista=[]
    dic={}
    for entry in queryset:
        year=entry['tupa_office_end__document_tupa__created'].year
        print(year)
        month=entry['tupa_office_end__document_tupa__created'].month
        day=entry['tupa_office_end__document_tupa__created'].day

        date_year=parse_date(date).year
        date_month = parse_date(date).month
        date_day= parse_date(date).day

        if (int(day) == int(date_day)) and (int(month) == int(date_month)) and (int(year )== int(date_year)):

            id_tupa = models.Tupa.objects.values('tup_des').filter(pk=entry['tupa_office_end__document_tupa__id_tupa'])
            ofi_des_begin = models.Office.objects.values('ofi_des').filter(
                pk=entry['tupa_office_end__id_ofi_begin__id'])
            ofi_des_end = models.Office.objects.values('ofi_des').filter(pk=entry['tupa_office_end__id_ofi_end__id'])
            id_person = models.Person.objects.values('per_name', 'per_lastname').filter(
                pk=entry['tupa_office_end__document_tupa__id_person_id'])

            dic['id'] = entry['tupa_office_end__document_tupa__id']
            dic['doc_number'] = entry['tupa_office_end__document_tupa__doc_number']
            dic['doc_exp_number'] = entry['tupa_office_end__document_tupa__doc_exp_number']
            dic['doc_pages'] = entry['tupa_office_end__document_tupa__doc_pages']
            dic['id_tupa'] = id_tupa[0]['tup_des']

            dic['id_person'] = str(id_person[0]['per_name'] + " " + id_person[0]['per_lastname'])
            dic['doc_begin'] = ofi_des_begin[0]['ofi_des']
            dic['doc_des'] = ofi_des_end[0]['ofi_des']
            dic['created'] = entry['tupa_office_end__document_tupa__created']
            lista.append(dic.copy())

        else:
            print("noo entra")
            continue
    #data = {'documentos': lista}
    return HttpResponse(lista)


@login_required(redirect_field_name='my_redirect_field')
def recibidosUsers(request):
    username = None
    if request.user.is_authenticated:

        username = request.user.username
        queryset = models.Office.objects.values('id', 'tupa_office_end__document_tupa__doc_number',
                                                'tupa_office_end__document_tupa__doc_exp_number',
                                                'tupa_office_end__document_tupa__doc_pages',
                                                'tupa_office_end__document_tupa__id_tupa'
                                                , 'tupa_office_end__document_tupa__id_person_id',
                                                'tupa_office_end__id_ofi_begin__id',
                                                'tupa_office_end__id_ofi_end__id',
                                                'tupa_office_end__document_tupa__doc_des',
                                                'tupa_office_end__document_tupa__id',
                                                'tupa_office_end__document_tupa__created').filter(
            ofi_des__icontains=username)

        lista = []
        for entry in queryset:
            try:
                dic = {}
                id_tupa = models.Tupa.objects.values('tup_des').filter(pk=entry['tupa_office_end__document_tupa__id_tupa'])
                ofi_des_begin = models.Office.objects.values('ofi_des').filter(pk=entry['tupa_office_end__id_ofi_begin__id'])
                ofi_des_end = models.Office.objects.values('ofi_des').filter(pk=entry['tupa_office_end__id_ofi_end__id'])
                id_person = models.Person.objects.values('per_name', 'per_lastname').filter(pk=entry['tupa_office_end__document_tupa__id_person_id'])
                dic['id'] = entry['tupa_office_end__document_tupa__id']
                dic['doc_number'] = entry['tupa_office_end__document_tupa__doc_number']
                dic['doc_exp_number'] = entry['tupa_office_end__document_tupa__doc_exp_number']
                dic['doc_pages'] = entry['tupa_office_end__document_tupa__doc_pages']
                dic['id_tupa'] = id_tupa[0]['tup_des']

                dic['id_person'] = str(id_person[0]['per_name'] + " " + id_person[0]['per_lastname'])
                dic['doc_begin'] = ofi_des_begin[0]['ofi_des']
                dic['doc_des'] = ofi_des_end[0]['ofi_des']
                dic['created'] = entry['tupa_office_end__document_tupa__created']

                lista.append(dic.copy())
            except:
                continue
        # return HttpResponse(dic)

        data = {'documentos': lista}
        return render(request, 'dmp/recibidos.html', data)
        # return HttpResponse(lista)

    else:
        return HttpResponse("No esta logeado")

    # return render(request, 'dusers/enviados.html', data)

@login_required(redirect_field_name='my_redirect_field')
def imprimirHojaTramite(request):
    data={}
    latest_id = models.Person.objects.latest('id')
    #return JsonResponse({'datos': {'id': latest_id.id, 'nombres': latest_id.per_name + " " + latest_id.per_lastname,'dni': latest_id.per_doc}})

    data['home'] = 'active'
    return render(request, 'dmp/print.html', {'datos': data, })

def update_movements(request,id_doc,id_tupa):
    query=models.Movements.objects.values('id').filter(id_doc__exact=id_doc,mov_order__exact=0)
    query_tupa=models.Tupa.objects.values('id_ofi_begin','id_ofi_end').filter(id=id_tupa)
    #return HttpResponse(query_tupa)
    return JsonResponse({'datos':{'id_movement': query[0]['id'], 'tupa_id': query_tupa[0]}})

@login_required(redirect_field_name='my_redirect_field')
def HojaTramite(request,id_doc):
    data={}
    latest_id = models.Document.objects.values('id').filter(pk=id_doc)


    return render(request, 'dmp/hojaTramite.html', {'datos':latest_id})


@login_required(redirect_field_name='my_redirect_field')
def BandejaEntrada(request):
    username = None
    if request.user.is_authenticated:

        username = request.user.username
        pk_username=models.Office.objects.values('id').filter(ofi_des__icontains=username)
        queryset_movements=models.Movements.objects.values('id_doc').filter(id_ofi_end__exact=pk_username[0]['id']).filter(move_recibed__exact=1)
        lista=[]
        for entry_queryset in queryset_movements:
            #print(entry_queryset['id_doc'])
            try:
                queryset = models.Office.objects.values('id', 'tupa_office_end__document_tupa__doc_number',
                                                        'tupa_office_end__document_tupa__doc_exp_number',
                                                        'tupa_office_end__document_tupa__doc_pages',
                                                        'tupa_office_end__document_tupa__id_tupa'
                                                        , 'tupa_office_end__document_tupa__id_person_id',
                                                        'tupa_office_end__id_ofi_begin__id',
                                                        'tupa_office_end__id_ofi_end__id',
                                                        'tupa_office_end__document_tupa__doc_des',
                                                        'tupa_office_end__document_tupa__id',
                                                        'tupa_office_end__document_tupa__created').filter(
                    tupa_office_end__document_tupa__id__exact=entry_queryset['id_doc'])
            except:
                continue

        for entry in queryset:
            dic = {}
            id_tupa = models.Tupa.objects.values('tup_des').filter(pk=entry['tupa_office_end__document_tupa__id_tupa'])
            ofi_des_begin = models.Office.objects.values('ofi_des').filter(pk=entry['tupa_office_end__id_ofi_begin__id'])
            ofi_des_end = models.Office.objects.values('ofi_des').filter(pk=entry['tupa_office_end__id_ofi_end__id'])
            id_person = models.Person.objects.values('per_name', 'per_lastname').filter(pk=entry['tupa_office_end__document_tupa__id_person_id'])
            dic['id'] = entry['tupa_office_end__document_tupa__id']
            dic['doc_number'] = entry['tupa_office_end__document_tupa__doc_number']
            dic['doc_exp_number'] = entry['tupa_office_end__document_tupa__doc_exp_number']
            dic['doc_pages'] = entry['tupa_office_end__document_tupa__doc_pages']
            dic['id_tupa'] = id_tupa[0]['tup_des']

            dic['id_person'] = str(id_person[0]['per_name'] + " " + id_person[0]['per_lastname'])
            dic['doc_begin'] = ofi_des_begin[0]['ofi_des']
            dic['doc_des'] = ofi_des_end[0]['ofi_des']
            dic['created'] = entry['tupa_office_end__document_tupa__created']

            lista.append(dic.copy())


        data = {'documentos': lista}
        return render(request, 'dmp/bandejaEntrada.html', data)

        #return HttpResponse(lista)

    else:
        return HttpResponse("No esta logeado")

