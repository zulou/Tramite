"""Tramite URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from . import routes
from Core import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    path('api/', include(routes)),
    #path('index/', views.index, name='index'),
    #path('login/', views.login, name='login'),
    #path('dashboard/', views.base, name='dashboard'),
    #path('dashboardUsers/', views.dashboard_users, name='dashboard_users'),

    path('dashboardMp/', views.dashboard_mesa_partes, name='dashboard_mesa_partes'),
    path('expedientesMp/', views.mesa_partes_expediente, name='expediente_mesa_partes'),
    path('accounts/', include('django.contrib.auth.urls')),

    path('get_provincias/<id>/', views.get_provincias, name='get_provincias'),
    path('get_departamentos/', views.get_departamentos, name='get_departamentos'),
    path('get_distritos/<id>/', views.get_distritos, name='get_distritos'),
    path('get_distritos/<id>/', views.get_distritos, name='get_distritos'),
    path('get_last_person/', views.get_last_insert_person, name='get_last_person'),
    path('get_dni_autocomplete/<dni>/', views.get_dni_autocomplete, name='get_dni_autocomplete'),
    path('get_person_dni/<dni>/', views.get_person_dni, name='get_person_dni'),
    path('get_tupa_autocomplete/<tupa>/', views.get_tupa_autocomplete, name='get_tupa_autocomplete'),
    path('register_attachment/', views.register_attachment, name='register_attachment'),
    path('get_last_document/', views.get_last_document, name='get_last_document'),
    path('get_last_document_movement/', views.get_last_document_movement, name='get_last_document_movement'),
    path('get_id_office/<office>/<date>/', views.get_id_office, name='get_id_office'),
    path('enviadosMp/', views.enviadosMp, name='expedientes_enviados'),
    path('comformidadMp/', views.comformidadMp, name='cargo_conformidad'),
    path('get_documentos_conformidad/<id>/<date>/', views.get_documentos_conformidad, name='get'),
    path('BandejaEntradaUsers/', views.recibidosUsers, name='expedientes_recibidos_users'),

    path('imprimirHojaTramite/', views.imprimirHojaTramite, name='imprimir_hoja_tramite'),

    path('update_movements/<id_doc>/<id_tupa>/', views.update_movements, name='update_movements'),
    path('HojaTramite/<id_doc>/', views.HojaTramite, name='hoja_tramite'),
    path('BandejaEntrada/', views.BandejaEntrada, name='bandeja_entrada'),



]


