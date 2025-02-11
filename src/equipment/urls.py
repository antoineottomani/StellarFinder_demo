from django.urls import path
from .views import calculate_and_save_fov, SaveFramingView

urlpatterns = [
    path('calcul-fov/<int:telescope_id>/<int:camera_id>/',
         calculate_and_save_fov, name="calcul-fov"),
    path('enregistrer-cadrage/', SaveFramingView.as_view(),
         name="enregistrer-cadrage"),
]
