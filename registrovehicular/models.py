import os

from django.db import models
from django.utils.timezone import now as timezone_now


class Vehiculo(models.Model):
    TYPE_VEHICULOS = (
        ("Moto", "Moto"),
        ("Camion", "Camion"),
        ("Panel", "Panel"),
        ("personal", "personal"),
    )
    TYPE_DIVISON = (("Farma", "Farma"), ("Consumo", "Consumo"))
    placa = models.CharField(max_length=10, blank=False, unique=True)
    marca = models.CharField(max_length=255, blank=False)
    tipo = models.CharField(max_length=256, choices=TYPE_VEHICULOS, default="Camion")
    estado_disponibilidad = models.BooleanField(default=True)
    division = models.CharField(max_length=256, choices=TYPE_DIVISON, default="Farma")
    estado_taller = models.BooleanField(default=False)
    creado = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    modificado = models.DateTimeField(auto_now=True, null=True, blank=True)

    def __str__(self):
        return self.placa

    class Meta:
        verbose_name_plural = "Vehiculos"
        verbose_name = "Vehiculo"


class Empleado(models.Model):
    TYPE_EMPLEADO = (
        ("Ayudante", "Ayudante"),
        ("Conductor", "Conductor"),
        ("Guardia", "Guardia"),
    )
    numero_empleado = models.CharField(max_length=10, blank=False, unique=True)
    nombre_completo = models.CharField(max_length=256, blank=False)
    tipo_empleado = models.CharField(
        max_length=256, choices=TYPE_EMPLEADO, default="Ayudante"
    )
    creado = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    actualizado = models.DateTimeField(auto_now=True, null=True, blank=True)

    def __str__(self):
        return f"{self.numero_empleado} - {self.nombre_completo}"

    class Meta:
        verbose_name_plural = "Empleados"
        verbose_name = "Empleado"


class ControlVehicular(models.Model):
    vehiculo = models.ForeignKey(Vehiculo, on_delete=models.CASCADE)
    empleados = models.ManyToManyField(Empleado)
    supervisor_salida = models.CharField(max_length=256)
    hora_salida = models.TimeField(auto_now_add=True)
    hora_entrada = models.TimeField(null=True, blank=True)
    fecha = models.DateField(auto_now_add=True)
    estatus = models.BooleanField(default=True)
    creado = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    actualizado = models.DateTimeField(auto_now=True, null=True, blank=True)

    def __str__(self):
        return self.vehiculo.placa

    class Meta:
        verbose_name_plural = "ControlesVehiculares"
        verbose_name = "ControlVehicular"


def upload_profile(instance, filename):
    now = timezone_now()
    filename_base, filename_ext = os.path.splitext(filename)
    time_stamp = now.strftime("%d%H%M%S")
    pk = str(getattr(instance, "pk"))
    return "registrovehicular/FotoEmpleados/%s_%s%s" % (
        pk,
        time_stamp,
        filename_ext.lower(),
    )


class FotosControlVehicular(models.Model):
    control_vehicular = models.ForeignKey(ControlVehicular, on_delete=models.CASCADE)
    foto_conductor_salida = models.ImageField(
        upload_to=upload_profile, blank=False, null=False
    )
    foto_ayudante1_salida = models.ImageField(
        upload_to=upload_profile, blank=True, null=True
    )
    foto_ayudante2_salida = models.ImageField(
        upload_to=upload_profile, blank=True, null=True
    )
    foto_conductor_entrada = models.ImageField(
        upload_to=upload_profile,
        blank=True,
        null=True,
    )
    foto_ayudante1_entrada = models.ImageField(
        upload_to=upload_profile,
        blank=True,
        null=True,
    )
    foto_ayudante2_entrada = models.ImageField(
        upload_to=upload_profile, blank=True, null=True
    )
    descripcion = models.TextField(blank=True, null=True)
