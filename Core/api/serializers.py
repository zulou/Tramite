from rest_framework import serializers
from Core import models

class Departamentoserializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = models.Departamento
        fields = ('departamento',)

class Provinciaserializer(serializers.HyperlinkedModelSerializer):
    id_departamento = serializers.PrimaryKeyRelatedField(many=False, queryset=models.Departamento.objects.all())
    class Meta:
        model = models.Provincia
        fields = ('id','id_departamento','provincia')


class Distritoserializer(serializers.HyperlinkedModelSerializer):
    id_provincia = serializers.PrimaryKeyRelatedField(many=False, queryset=models.Provincia.objects.all())
    class Meta:
        model = models.Distrito
        fields = ('id','id_provincia','distrito')

class Officeserializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = models.Office
        fields = ('id','ofi_des',)


class Tupaserializer(serializers.HyperlinkedModelSerializer):
    id_ofi_begin = serializers.PrimaryKeyRelatedField(many=False, queryset=models.Office.objects.all())
    id_ofi_end = serializers.PrimaryKeyRelatedField(many=False, queryset=models.Office.objects.all())

    class Meta:
        model = models.Tupa
        fields = ('id','id_ofi_begin', 'id_ofi_end', 'tup_des', 'tup_requeriments', 'tup_cost', 'tup_days')


class Type_documentserializer(serializers.HyperlinkedModelSerializer):
    #id=serializers.Field()
    class Meta:
        model = models.Type_document
        fields = ('id','doc_des')

class Document_identityserializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = models.Document_identity
        fields = ('id','doc_des')


class Personserializer(serializers.HyperlinkedModelSerializer):
    #user = serializers.PrimaryKeyRelatedField(many=False, queryset=models.User.objects.all())
    id_doc = serializers.PrimaryKeyRelatedField(many=False, queryset=models.Document_identity.objects.all())
    id_departamento= serializers.PrimaryKeyRelatedField(many=False, queryset=models.Departamento.objects.all())
    id_provincia = serializers.PrimaryKeyRelatedField(many=False, queryset=models.Provincia.objects.all())
    id_distrito = serializers.PrimaryKeyRelatedField(many=False, queryset=models.Distrito.objects.all())

    class Meta:
        model = models.Person
        fields = ('id','id_doc','id_departamento', 'id_provincia','id_distrito','per_name', 'per_lastname', 'per_doc', 'per_cellphone', 'per_type')


class Documentserializer(serializers.HyperlinkedModelSerializer):
    id_type_document = serializers.PrimaryKeyRelatedField(many=False, queryset=models.Type_document.objects.all())
    id_person = serializers.PrimaryKeyRelatedField(many=False, queryset=models.Person.objects.all())
    id_tupa = serializers.PrimaryKeyRelatedField(many=False, queryset=models.Tupa.objects.all())

    class Meta:
        model = models.Document
        fields = ('id',
            'id_type_document', 'id_person', 'id_tupa', 'doc_number', 'doc_exp_number', 'doc_des', 'doc_pages',
            'doc_type','doc_status')

class Attachmentsserializer(serializers.HyperlinkedModelSerializer):
    id_doc = serializers.PrimaryKeyRelatedField(many=False, queryset=models.Document.objects.all())
    class Meta:
        model = models.Attachments
        fields = ('id','id_doc','att_path',)


class Movementsserializer(serializers.HyperlinkedModelSerializer):
    id_doc = serializers.PrimaryKeyRelatedField(many=False, queryset=models.Document.objects.all())
    class Meta:
        model = models.Movements
        fields = ('id','id_doc','mov_order', 'id_attachments', 'id_ofi_begin', 'id_ofi_end', 'id_doc_sender', 'move_recibed')