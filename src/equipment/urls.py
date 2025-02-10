from django.urls import path
from .views import CreateTelescope, ListTelescope, UpdateTelescope, DeleteTelescope
from .views import CreateCamera, ListCamera, UpdateCamera, DeleteCamera
from .views import calculate_and_save_fov, SaveFramingView

urlpatterns = [
    path('telescope/liste', ListTelescope.as_view(), name="liste-telescope"),
    path('telescope/ajouter/', CreateTelescope.as_view(), name="ajouter-telescope"),
    path('telescope/modifier/<int:pk>/',
         UpdateTelescope.as_view(), name="modifier-telescope"),
    path('telescope/supprimer/<int:pk>/',
         DeleteTelescope.as_view(), name="supprimer-telescope"),
    path('camera/liste', ListCamera.as_view(), name="liste-camera"),
    path('camera/ajouter/', CreateCamera.as_view(), name="ajouter-camera"),
    path('camera/modifier/<int:pk>/',
         UpdateCamera.as_view(), name="modifier-camera"),
    path('camera/supprimer/<int:pk>/',
         DeleteCamera.as_view(), name="supprimer-camera"),
    path('calcul-fov/<int:telescope_id>/<int:camera_id>/',
         calculate_and_save_fov, name="calcul-fov"),
    path('enregistrer-cadrage/', SaveFramingView.as_view(),
         name="enregistrer-cadrage"),
]
