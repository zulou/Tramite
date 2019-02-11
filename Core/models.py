from django.db import models
from django.contrib.auth.models import User

# Create your models here.


class Departamento(models.Model):
    departamento = models.CharField(max_length=20, null=False)
    def __str__(self):
        return(self.departamento)

class Provincia(models.Model):
    id_departamento = models.ForeignKey(Departamento, on_delete=models.CASCADE, related_name="provincia_departamento")
    provincia = models.CharField(max_length=20, null=False)
    def __str__(self):
        return(self.provincia)


class Distrito(models.Model):
    id_provincia=models.ForeignKey(Provincia, on_delete=models.CASCADE, related_name="tupa_office_begin")
    distrito = models.CharField(max_length=30, null=False)
    def __str__(self):
        return(self.distrito)

class Office(models.Model):
    ofi_des = models.CharField(max_length=40, null=False)
    def __str__(self):
        return(self.ofi_des)

class Tupa(models.Model):
    id_ofi_begin = models.ForeignKey(Office, on_delete=models.CASCADE, related_name="tupa_office_begin")
    id_ofi_end = models.ForeignKey(Office, on_delete=models.CASCADE, related_name="tupa_office_end")
    tup_des = models.CharField(max_length=60,null=False)
    tup_requeriments= models.CharField(max_length=20,null=False)
    tup_cost= models.CharField(max_length=20,null=False)
    tup_days= models.CharField(max_length=20,null=False)
    def __str__(self):
        return(self.tup_des)


class Type_document(models.Model):
    doc_des= models.CharField(max_length=20, null=False)
    def __str__(self):
        return(self.doc_des)

class Movements(models.Model):
    mov_order = models.IntegerField( null=False)
    id_attachments = models.IntegerField( null=False)
    id_ofi_begin = models.IntegerField( null=False)
    id_ofi_end = models.IntegerField( null=False)
    id_doc_sender = models.IntegerField( null=False)
    move_recibed = models.IntegerField( null=False)




class Document_identity(models.Model):
    doc_des= models.CharField(max_length=20, null=False)
    def __str__(self):
        return(self.doc_des)

class Person(models.Model):
    #user=models.OneToOneField(User,on_delete=models.CASCADE)
    id_doc = models.ForeignKey(Document_identity, on_delete=models.CASCADE, related_name="person_document_identity")
    id_departamento=models.ForeignKey(Departamento, on_delete=models.CASCADE, related_name="person_departamento")
    id_provincia=models.ForeignKey(Provincia, on_delete=models.CASCADE, related_name="person_provincia")
    id_distrito=models.ForeignKey(Distrito, on_delete=models.CASCADE, related_name="person_distrito")
    per_name = models.CharField(max_length=20, null=False)
    per_lastname = models.CharField(max_length=20, null=False)
    per_doc = models.CharField(unique=True,max_length=20, null=False)
    per_cellphone = models.CharField(max_length=20, null=False)
    per_type = models.CharField(max_length=20, null=False)
    def __str__(self):
        return(str(self.id_doc)+" "+self.per_name)



class Document (models.Model):
    id_type_document = models.ForeignKey(Type_document,on_delete=models.CASCADE,related_name="document_type_document")
    id_person = models.ForeignKey(Person, on_delete=models.CASCADE, related_name="document_person")
    id_tupa = models.ForeignKey(Tupa, on_delete=models.CASCADE, related_name="document_tupa")
    doc_number= models.CharField(max_length=20, null=False)
    doc_exp_number = models.IntegerField(null=True)
    doc_des = models.CharField(max_length=50, null=False)
    doc_pages = models.IntegerField( null=False)
    doc_type= models.IntegerField( null=False)

    def __str__(self):
        return(str(self.id_type_document)+" "+str(self.id_person)+" "+str(self.id_tupa))

    def save(self, *args, **kwargs):
        qs=Document.objects.last()
        if qs is None:
            self.doc_exp_number=1
        else:

            self.doc_exp_number=qs.doc_exp_number+1
        super(Document,self).save()


class Attachments(models.Model):
    id_doc = models.ForeignKey(Document, on_delete=models.CASCADE, related_name="attachments_document")
    att_path= models.CharField(max_length=20, null=False)
    def __str__(self):
        return(self.att_path)


class Movements(models.Model):
    id_doc = models.ForeignKey(Document, on_delete=models.CASCADE, related_name="movements_document")
    mov_order = models.IntegerField( null=False)
    id_attachments = models.IntegerField( null=False)
    id_ofi_begin = models.IntegerField( null=False)
    id_ofi_end = models.IntegerField( null=False)
    id_doc_sender = models.IntegerField( null=False)
    move_recibed = models.IntegerField( null=False)