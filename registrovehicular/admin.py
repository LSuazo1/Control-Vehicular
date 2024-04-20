from django.contrib import admin

from .models import Empleado,Vehiculo,ControlVehicular,FotosControlVehicular

@admin.register(Empleado)
class EmpleadoAdmin(admin.ModelAdmin):
    list_display = ("numero_empleado","nombre_completo","tipo_empleado","creado","actualizado")
    ordering =("numero_empleado","nombre_completo","tipo_empleado","creado","actualizado")
    search_fields = ("numero_empleado","nombre_completo","tipo_empleado")