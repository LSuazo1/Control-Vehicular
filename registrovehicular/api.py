from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.decorators import action
import datetime
from .models import Vehiculo, Empleado, ControlVehicular, FotosControlVehicular
from .serializers import (
    VehiculoSerializer,
    EmpleadoSerializer,
    ControlVehicularSerializer,
    FotosControlVehicularSerializer,
)


class VehiculoViewSet(viewsets.ModelViewSet):
    queryset = Vehiculo.objects.all()
    serializer_class = VehiculoSerializer


class EmpleadoViewSet(viewsets.ModelViewSet):
    queryset = Empleado.objects.all()
    serializer_class = EmpleadoSerializer

    # Método para buscar empleados por su número de empleado
    @action(detail=False, methods=["get"])
    def buscar_codigo_empleado(self, request):
        numero_empleado = request.query_params.get("numero_empleado", None)
        if numero_empleado:
            empleados = self.queryset.filter(numero_empleado=numero_empleado)
            serializer = self.get_serializer(empleados, many=True)
            return Response(serializer.data)
        else:
            return Response(
                {"error": {'message':'Se requiere el parámetro "numero_empleado" en la consulta.'}},
                status=400,
            )


class ControlVehicularViewSet(viewsets.ModelViewSet):
    queryset = ControlVehicular.objects.all()
    serializer_class = ControlVehicularSerializer

    @action(detail=False, methods=["post"])
    def guardar_registro(self, request):
        codigoAyudante1 = request.data.get("ayudante1", None)
        codigoAyudante2 = request.data.get("ayudante2", None)
        codigoConductor = request.data.get("codigoConductor", None)
        supervisorSalida = request.data.get("supervisorSalida", None)
        taller = request.data.get("taller", None)
        placa = request.data.get("placaVehiculo", None)
        print(placa,codigoConductor)
       
        if codigoConductor is None:
            error_message = {"error": {"message": "Es necesario que mande un conductor."}}
            print(error_message)
            return Response(error_message, status=400)
        
        if supervisorSalida is None:
            error_message = {"error": { "message": "Es necesario que mande el supervisor."}}
            print(error_message)
            return Response(error_message, status=400)
        
        if codigoConductor is not None:
            try:
                conductor = Empleado.objects.get(numero_empleado=int(codigoConductor))
                print(conductor)
            except Exception as e:
                error_message = {"error": { "message": "No se encontró ningún Conductor con el codigo proporcionado"}}
                print(e)
                return Response(error_message, status=404)
            
        try:
            vehiculo = Vehiculo.objects.get(placa=placa)
            if not vehiculo.estado_disponibilidad:
               error_message = {"error": { "message": "El vehículo no está disponible."}}
               print(error_message)
               return Response(error_message, status=400)
            
            vehiculo.estado_disponibilidad = False
            vehiculo.save() 

        except Vehiculo.DoesNotExist:
            error_message = {"error": {"message": "No se encontró ningún vehículo con la placa proporcionada"}}
            print(error_message)
            return Response(error_message, status=404)
        
        
        control_vehicular = ControlVehicular.objects.create(
            vehiculo=vehiculo,
        )

        if taller is not None:
             control_vehicular.taller=taller
             vehiculo.estado_taller=True
             vehiculo.save() 

        control_vehicular.empleados.add(conductor)

        if supervisorSalida is not None:
            try:
                supervisor = Empleado.objects.get(numero_empleado=supervisorSalida)
                print(supervisor.getNombre())
                control_vehicular.supervisor_salida=supervisor.nombre_completo
                control_vehicular.save()
            except Exception as e:
                error_message = {"error": { "message": "No se encontró ningún Supervisor con el codigo proporcionado"}}
                print(e)
                return Response(error_message, status=404)
        
            
        if codigoAyudante1 is not None:
            try:
                ayudante1 = Empleado.objects.get(numero_empleado=codigoAyudante1)
                control_vehicular.empleados.add(ayudante1)
            except Empleado.DoesNotExist:
                error_message = {"error": {"message": "No se encontró ningún Ayudante1 con el codigo proporcionado"}}
                print(error_message)
                return Response(error_message, status=404)
        
        if codigoAyudante2 is not None:
            try:
                ayudante2 = Empleado.objects.get(numero_empleado=codigoAyudante2)
                control_vehicular.empleados.add( ayudante2)
            except Empleado.DoesNotExist:
                error_message = {"error": { "message": "No se encontró ningún Ayudante2 con el codigo proporcionado"}}
                print(error_message)
                return Response(error_message, status=404)

        serializer = ControlVehicularSerializer(control_vehicular)

        return Response(serializer.data, status=201)

    @action(detail=False, methods=["patch"])
    def actualizar_registro(self, request):
        codigoAyudante1 = request.data.get("ayudante1", None)
        codigoAyudante2 = request.data.get("ayudante2", None)
        codigoConductor = request.data.get("codigoConductor", None)
        placa = request.data.get("placaVehiculo", None)
        print(placa)
        if codigoConductor is None:
            error_message = {"error": {"message": "Es necesario que mande un conductor."}}
            print(error_message)
            return Response(error_message, status=400)
        
        try:
            conductor = Empleado.objects.get(numero_empleado=codigoConductor)
        except Empleado.DoesNotExist:
            error_message = {"error": {"message": "El conductor especificado no existe."}}
            print(error_message)
            return Response(error_message, status=404)
        
        if codigoAyudante1:
            try:
                ayudante1 = Empleado.objects.get(numero_empleado=codigoAyudante1)
            except Empleado.DoesNotExist:
                error_message = {"error": {"message": "El ayudante 1 especificado no existe."}}
                print(error_message)
                return Response(error_message, status=404)

        # Verificar si se proporcionó el código del ayudante 2
        if codigoAyudante2:
            try:
                ayudante2 = Empleado.objects.get(numero_empleado=codigoAyudante2)
            except Empleado.DoesNotExist:
                error_message = {"error": {"message": "El ayudante 2 especificado no existe."}}
                print(error_message)
                return Response(error_message, status=404)
            

        try:
            vehiculo = Vehiculo.objects.get(placa=placa)
            if  vehiculo.estado_taller:
                vehiculo.estado_taller =False
            
            vehiculo.estado_disponibilidad = True
            vehiculo.save() 

        except Vehiculo.DoesNotExist:
            error_message = {"error": {"message": "No se encontró ningún vehículo con la placa proporcionada"}}
            print(error_message)
            return Response(error_message, status=404)    
        
        try:
            controlVehicular = ControlVehicular.objects.filter(vehiculo__placa=placa).latest('creado')
            controlVehicular.hora_entrada=datetime.datetime.now().time().strftime('%I:%M %p')
            print(datetime.datetime.now().time().strftime('%I:%M %p'))
            controlVehicular.estatus=False
            controlVehicular.save()
        except Exception as e:
                error_message = {"error": { "message": "No se encontró ningún Control vehicular con la placa proporcionada"}}
                print(e)
                return Response(error_message, status=404)
        
        serializer = ControlVehicularSerializer(controlVehicular)

        return Response(serializer.data, status=200)



        

class VehiculoViewSet(viewsets.ModelViewSet):
    queryset = Vehiculo.objects.all()
    serializer_class = VehiculoSerializer

    @action(detail=False, methods=["get"])
    def buscar_por_placa(self, request):
        placa = request.query_params.get("placa", None)
        if placa:
            vehiculo = Vehiculo.objects.filter(placa=placa).first()
            if vehiculo:
                serializer = self.get_serializer(vehiculo)
                return Response(serializer.data)
            else:
                return Response(
                    {"error": {"message":"No se encontró ningún vehículo con esa placa."}},
                    status=404,
                )
        else:
            return Response(
                {"error": {"message":'Se requiere el parámetro "placa" en la consulta.'}},
                status=400,
            )


class FotosControlVehicularViewSet(viewsets.ModelViewSet):
    queryset = FotosControlVehicular.objects.all()
    serializer_class = FotosControlVehicularSerializer

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop("partial", False)
        instance = self.get_object()
        control_vehicular_id = request.data.get("control_vehicular", None)
        if control_vehicular_id is not None:
            instance.control_vehicular_id = control_vehicular_id
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(serializer.data)

    def perform_update(self, serializer):
        serializer.save()

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response(status=204)


    @action(detail=False, methods=['get'])
    def buscar_por_control_vehicular(self, request):
        control_vehicular_id = request.query_params.get('id', None)
        if control_vehicular_id is not None:
            fotos = self.queryset.filter(control_vehicular_id=control_vehicular_id)
            serializer = self.get_serializer(fotos, many=True)
            return Response(serializer.data)
        else:
            return Response(
                {"error": {"message":"Se requiere el ID del control vehicular en la consulta."}},
                status=400,
            )
        
    
    @action(detail=False, methods=["patch"])
    def actualizar_fotos_entrada(self, request):
        control_vehicular_id = request.query_params.get("control_id", None)
        print(control_vehicular_id)
        if control_vehicular_id is None:
            return Response(
                {"error": {"message":"Se requiere el ID del control vehicular para actualizar las fotos de entrada."}},
                status=400
            )

        fotos_entrada = FotosControlVehicular.objects.filter(
            control_vehicular_id=control_vehicular_id
        ).first()

       
        if fotos_entrada is None:
            return Response(
                {"error": {"message":"No se encontraron fotos de entrada para el control vehicular proporcionado."}},
                status=404
            )

        # Actualizar las fotos de entrada si se proporcionaron en la solicitud
        if "foto_conductor_entrada" in request.data:
            fotos_entrada.foto_conductor_entrada = request.data["foto_conductor_entrada"]
        if "foto_ayudante1_entrada" in request.data:
            fotos_entrada.foto_ayudante1_entrada = request.data["foto_ayudante1_entrada"]
        if "foto_ayudante2_entrada" in request.data:
            fotos_entrada.foto_ayudante2_entrada = request.data["foto_ayudante2_entrada"]
        
        fotos_entrada.save()

        serializer = self.get_serializer(fotos_entrada)
        return Response(serializer.data)
    
    @action(detail=False, methods=["post"])
    def guardar_fotos(self, request):
        control_vehicular_id = request.query_params.get("control_id", None)
        print(control_vehicular_id)
        if control_vehicular_id is None:
            return Response(
                {"error": {"message":"Se requiere el ID del control vehicular para actualizar las fotos de entrada."}},
                status=400
            )
        
        if "foto_conductor_salida" not in request.data:
            return Response(
                {"error": {"message":"Se requiere la foto del conductor para guardar las fotos de entrada."}},
                status=400
            )

        try:
            fotos_entrada, created = FotosControlVehicular.objects.get_or_create(
                control_vehicular_id=control_vehicular_id
            )

            print("foto del conductor:",request.data["foto_conductor_salida"])

            fotos_entrada.foto_conductor_salida = request.data["foto_conductor_salida"]

            if "foto_ayudante1_salida" in request.data:
                fotos_entrada.foto_ayudante1_salida = request.data["foto_ayudante1_salida"]
            if "foto_ayudante2_salida" in request.data:
                fotos_entrada.foto_ayudante2_salida = request.data["foto_ayudante2_salida"]
            
            fotos_entrada.save()

            serializer = self.get_serializer(fotos_entrada)
            return Response(serializer.data, status=201)
        except Exception as e:
            return Response(
                {"error": {"message": str(e)}},
                status=500
            )