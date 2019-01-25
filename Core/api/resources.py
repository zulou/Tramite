from rest_framework import  viewsets
from Core import models
from . import serializers

class OfficeViewset(viewsets.ModelViewSet):
	queryset=models.Office.objects.all()
	serializer_class=serializers.Operadorserializer

class TupaViewset(viewsets.ModelViewSet):
	queryset=models.Tupa.objects.all()
	serializer_class=serializers.Turnoserializer


class Type_documentViewset(viewsets.ModelViewSet):
    queryset = models.Type_document.objects.all()
    serializer_class = serializers.Equiposerializer

class AttachmentsViewset(viewsets.ModelViewSet):
    queryset = models.Attachments.objects.all()
    serializer_class = serializers.Actividadserializer


class MovementsViewset(viewsets.ModelViewSet):
    queryset = models.Movements.objects.all()
    serializer_class = serializers.Detalle_actividadserializer

class Document_identityViewset(viewsets.ModelViewSet):
    queryset = models.Document_identity.objects.all()
    serializer_class = serializers.Simbaserializer

class PersonViewset(viewsets.ModelViewSet):
    queryset = models.Person.objects.all()
    serializer_class = serializers.Scoopserializer

class DocumentViewset(viewsets.ModelViewSet):
    queryset = models.Document.objects.all()
    serializer_class = serializers.Scoopserializer

