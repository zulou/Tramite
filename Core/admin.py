from django.contrib import admin
from . import models


# Register your models here.

class DepartamentoAdmin(admin.ModelAdmin):
    search_fields = ['departamento']
    list_display = ('departamento',)

class ProvinciaAdmin(admin.ModelAdmin):
    search_fields = ['id_departamento','provincia']
    list_display = ('id_departamento','provincia',)

class DistritoAdmin(admin.ModelAdmin):
    search_fields = ['id_provincia','distrito']
    list_display = ('id_provincia','distrito',)

class OfficeAdmin(admin.ModelAdmin):
    search_fields = ['ofi_des']
    list_display = ('ofi_des',)

class TupaAdmin(admin.ModelAdmin):
    search_fields = ['id_ofi_begin', 'id_ofi_end', 'tup_des','tup_requeriments','tup_cost','tup_days']
    list_display = ('id_ofi_begin', 'id_ofi_end', 'tup_des','tup_requeriments','tup_cost','tup_days')

class Type_documentAdmin(admin.ModelAdmin):
    search_fields = ['doc_des']
    list_display = ('doc_des',)

class AttachmentsAdmin(admin.ModelAdmin):
    search_fields = ['att_path']
    list_display = ('att_path',)

class MovementsAdmin(admin.ModelAdmin):
    search_fields = ['mov_order','id_attachments','id_ofi_begin','id_ofi_end','id_doc_sender','move_recibed']
    list_display = ('mov_order','id_attachments','id_ofi_begin','id_ofi_end','id_doc_sender','move_recibed')

class Document_identityAdmin(admin.ModelAdmin):
    search_fields = ['doc_des']
    list_display = ('doc_des',)

class PersonAdmin(admin.ModelAdmin):
    search_fields = ['id_doc','per_name','per_lastname','per_doc','per_address','per_cellphone','per_type']
    list_display = ('id_doc','per_name','per_lastname','per_doc','per_address','per_cellphone','per_type')

class DocumentAdmin(admin.ModelAdmin):
    search_fields = ['id_type_document','id_person','id_tupa','doc_number','doc_exp_number','doc_des','doc_pages','doc_type']
    list_display = ('id_type_document','id_person','id_tupa','doc_number','doc_exp_number','doc_des','doc_pages','doc_type')



admin.site.register(models.Office,OfficeAdmin)
admin.site.register(models.Tupa,TupaAdmin)
admin.site.register(models.Type_document,Type_documentAdmin)
admin.site.register(models.Attachments,AttachmentsAdmin)
admin.site.register(models.Movements,MovementsAdmin)
admin.site.register(models.Document_identity,Document_identityAdmin)
admin.site.register(models.Person,PersonAdmin)
admin.site.register(models.Document,DocumentAdmin)

admin.site.register(models.Departamento,DepartamentoAdmin)
admin.site.register(models.Provincia,ProvinciaAdmin)
admin.site.register(models.Distrito,DistritoAdmin)
