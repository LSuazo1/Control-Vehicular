from rest_framework import serializers
from .models import Vehiculo, Empleado, ControlVehicular, FotosControlVehicular

class VehiculoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vehiculo
        fields = '__all__'

class EmpleadoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Empleado
        fields = '__all__'
        
class FotosControlVehicularSerializer(serializers.ModelSerializer):
    class Meta:
        model = FotosControlVehicular
        fields = '__all__'        

class ControlVehicularSerializer(serializers.ModelSerializer):
    fotos_control_vehicular = FotosControlVehicularSerializer(many=True, read_only=True)

    class Meta:
        model = ControlVehicular
        fields = '__all__'

class VehiculoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vehiculo
        fields = '__all__'


