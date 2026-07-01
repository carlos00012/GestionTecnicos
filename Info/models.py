from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Tecnico(models.Model):
    id = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=100)
    apellido = models.CharField(max_length=100)
    telefono = models.CharField(max_length=20)
    especialidad = models.CharField(max_length=100)
    foto = models.FileField(upload_to='fotos_tecnicos', blank=True, null=True)

    def __str__(self):
        return f"{self.nombre} - {self.apellido} - {self.telefono} - {self.especialidad}"

class Cursos(models.Model):
    id = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField()
    fecha_inicio = models.DateField()
    fecha_fin = models.DateField()
    tecnico = models.ForeignKey(Tecnico, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return f"{self.nombre} - {self.descripcion} - {self.fecha_inicio} - {self.fecha_fin} - {self.tecnico.nombre}"


class Perfil(models.Model):

    ROLES = (
        ('admin','Administrador'),
        ('tecnico','Tecnico'),
    )

    usuario = models.OneToOneField(User, on_delete=models.CASCADE)
    rol = models.CharField(max_length=20, choices=ROLES)


    def __str__(self):
        return self.usuario.username