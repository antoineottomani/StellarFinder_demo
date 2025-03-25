from django.urls import path
from .views import CalculateFOV

urlpatterns = [
    path('calcul-fov/<int:telescope_id>/<int:camera_id>/',
         CalculateFOV.as_view(), name="calcul-fov"),
]
