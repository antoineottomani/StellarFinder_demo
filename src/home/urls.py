from django.urls import path
from .views import proxy_to_aladin, FetchEquipment, homepage_view

urlpatterns = [
    path('', homepage_view, name="accueil"),
    path('proxy-aladin/', proxy_to_aladin, name="proxy vers aladin"),
    path('equipement/', FetchEquipment.as_view(), name="equipement"),
]
