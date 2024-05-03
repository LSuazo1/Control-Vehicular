from django.contrib import admin

from .models import Empleado,Vehiculo,ControlVehicular,FotosControlVehicular

@admin.register(Empleado)
class EmpleadoAdmin(admin.ModelAdmin):
    list_display = ("id","numero_empleado","nombre_completo","tipo_empleado","creado","actualizado")
    ordering =("numero_empleado","nombre_completo","tipo_empleado","creado","actualizado")
    search_fields = ("numero_empleado","nombre_completo","tipo_empleado")

@admin.register(Vehiculo)
class VehiculoAdmin(admin.ModelAdmin):
    list_display = ("id", "placa", "marca", "tipo", "estado_disponibilidad", "division", "estado_taller", "creado")
    ordering = ("id", "placa", "marca")
    search_fields = ("id", "placa", "marca", "tipo")

@admin.register(ControlVehicular)
class ControlVehicular(admin.ModelAdmin):
    list_display = ("id","vehiculo","supervisor_salida","hora_salida","hora_entrada","fecha","estatus","creado","actualizado")
    ordering = ("id", "vehiculo")
    search_fields = ("id", "vehiculo")
    readonly_fields = ("hora_salida", "fecha", "creado", "actualizado")

    def get_empleados(self, obj):
        return ", ".join([str(empleado) for empleado in obj.empleados.all()])

    get_empleados.short_description = "Empleados"

@admin.register(FotosControlVehicular)
class FotosControlVehicular(admin.ModelAdmin):
    list_display = ("id","control_vehicular","foto_conductor_salida","foto_ayudante1_salida","foto_ayudante2_salida","foto_conductor_entrada","foto_ayudante1_entrada","foto_ayudante2_entrada")
    ordering = ("id", "control_vehicular")
    search_fields = ("id", "control_vehicular")
    