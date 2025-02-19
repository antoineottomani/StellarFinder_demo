from django.urls import path
from .views import calculate_and_save_fov

urlpatterns = [
    path('calcul-fov/',
         calculate_and_save_fov, name="calcul-fov"),
]
