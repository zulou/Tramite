from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Office(models.Model):
    ofi_des = models.CharField(max_length=12, null=False)
    def __str__(self):
        return(self.ofi_des)

class Tupa(models.Model):
    id_ofi_begin = models.ForeignKey(Office, on_delete=models.CASCADE, related_name="tupa_office_begin")
    id_ofi_end = models.ForeignKey(Office, on_delete=models.CASCADE, related_name="tupa_office_end")
    tup_des = models.CharField(max_length=12,null=False)
    tup_requeriments= models.CharField(max_length=12,null=False)
    tup_cost= models.CharField(max_length=12,null=False)
    tup_days= models.CharField(max_length=12,null=False)


class Type_document(models.Model):
    doc_des= models.CharField(max_length=12, null=False)
    def __str__(self):
        return(self.doc_des)

class Attachments(models.Model):
    att_path= models.CharField(max_length=12, null=False)
    def __str__(self):
        return(self.att_path)

class Movements(models.Model):
    mov_order = models.IntegerField( null=False)
    id_attachments = models.IntegerField( null=False)
    id_ofi_begin = models.IntegerField( null=False)
    id_ofi_end = models.IntegerField( null=False)
    id_doc_sender = models.IntegerField( null=False)
    move_recibed = models.IntegerField( null=False)


class Document_identity(models.Model):
    doc_des= models.CharField(max_length=12, null=False)
    def __str__(self):
        return(self.doc_des)

class Person(models.Model):
    user=models.OneToOneField(User,on_delete=models.CASCADE)
    id_doc = models.ForeignKey(Document_identity, on_delete=models.CASCADE, related_name="person_document_identity")
    per_name = models.CharField(max_length=12, null=False)
    per_lastname = models.CharField(max_length=12, null=False)
    per_doc = models.CharField(max_length=12, null=False)
    per_address = models.CharField(max_length=12, null=False)
    per_cellphone = models.CharField(max_length=12, null=False)
    per_type = models.CharField(max_length=12, null=False)
    def __str__(self):
        return(str(self.id_doc)+" "+self.per_name)



class Document (models.Model):
    id_type_document = models.ForeignKey(Type_document,on_delete=models.CASCADE,related_name="document_type_document")
    id_person = models.ForeignKey(Person, on_delete=models.CASCADE, related_name="document_person")
    id_tupa = models.ForeignKey(Tupa, on_delete=models.CASCADE, related_name="document_tupa")
    doc_number= models.CharField(max_length=12, null=False)
    doc_exp_number = models.IntegerField( null=False)
    doc_des = models.CharField(max_length=12, null=False)
    doc_pages = models.IntegerField( null=False)
    doc_type= models.IntegerField( null=False)
