from django.db import models

class Usuarios(models.Model):
    nombre = models.CharField(max_length=50)
    correo = models.EmailField(unique=True)
    edad = models.IntegerField()
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    contrasena = models.CharField(max_length=50)
    def __str__(self):
        return self.nombre



