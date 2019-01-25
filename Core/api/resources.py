from rest_framework import  viewsets
from Core import models
from . import serializers

class OfficeViewset(viewsets.ModelViewSet):
	queryset=models.Office.objects.all()
	serializer_class=serializers.Officeserializer

class TupaViewset(viewsets.ModelViewSet):
	queryset=models.Tupa.objects.all()
	serializer_class=serializers.Tupaserializer


class Type_documentViewset(viewsets.ModelViewSet):
    queryset = models.Type_document.objects.all()
    serializer_class = serializers.Type_documentserializer

class AttachmentsViewset(viewsets.ModelViewSet):
    queryset = models.Attachments.objects.all()
    serializer_class = serializers.Attachmentsserializer


class MovementsViewset(viewsets.ModelViewSet):
    queryset = models.Movements.objects.all()
    serializer_class = serializers.Movementsserializer

class Document_identityViewset(viewsets.ModelViewSet):
    queryset = models.Document_identity.objects.all()
    serializer_class = serializers.Document_identityserializer

class PersonViewset(viewsets.ModelViewSet):
    queryset = models.Person.objects.all()
    serializer_class = serializers.Personserializer

class DocumentViewset(viewsets.ModelViewSet):
    queryset = models.Document.objects.all()
    serializer_class = serializers.Documentserializer

