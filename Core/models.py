from django.db import models

# Create your models here.

class operador(models.Model):
    nombre_operador = models.CharField(max_length=12,null=False)
    usuario = models.CharField(max_length=12,null=False)
    password = models.CharField(max_length=12,null=False)
    tipo_operador = models.CharField(max_length=12,null=False)
    def __str__(self):
        return(self.nombre_operador+" "+self.usuario+" "+self.password)

class turno(models.Model):
    descripcion_turno = models.CharField(max_length=12, null=False)
    def __str__(self):
        return(self.descripcion_turno)

class equipo(models.Model):
    nombre_equipo = models.CharField(max_length=12, null=False)
    modelo = models.CharField(max_length=12, null=False)
    estado = models.IntegerField(max_length=12,null=False)
    def __str__(self):
        return(self.nombre_equipo+" "+self.modelo+" ")

class actividad(models.Model):
    id_turno=models.ForeignKey(turno,on_delete=models.CASCADE,related_name="actividad_turno")
    id_operador = models.ForeignKey(operador,on_delete=models.CASCADE, related_name="actividad_operador")
    id_ayudante=models.ForeignKey(operador,on_delete=models.CASCADE, related_name="actividad_ayudante",null=True)
    id_equipo=models.ForeignKey(equipo,on_delete=models.CASCADE, related_name="actividad_equipo")
    fecha_actividad = models.DateField(blank=True, default=date.today)
    nivel = models.CharField(max_length=12, null=True)