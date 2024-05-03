from django.urls import path, include
from rest_framework import routers
from .api import VehiculoViewSet, EmpleadoViewSet, ControlVehicularViewSet, FotosControlVehicularViewSet


# Crear un enrutador
router = routers.DefaultRouter()

# Registrar los viewsets de tu aplicación principal y los nuevos viewsets
router.register("api/vehiculos", VehiculoViewSet, "vehiculos")
router.register("api/empleados", EmpleadoViewSet, "empleados")
router.register("api/controlvehicular", ControlVehicularViewSet, "controlvehicular")
router.register("api/fotoscontrolvehicular", FotosControlVehicularViewSet, "fotoscontrolvehicular")

urlpatterns = [
    path("", include(router.urls)),  # Incluir las URLs generadas por el enrutador
]