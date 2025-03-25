import json
import math
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views import View
from django.shortcuts import get_object_or_404
# from home.views import load_demo_data
from django.conf import settings


def load_demo_data():
    with open(settings.DEMO_DATA_PATH, "r") as file:
        return json.load(file)

# Calculate Field Of View(FOV)
class CalculateFOV(View):
    def get(self, request, telescope_id, camera_id, *args, **kwargs):
        try:
            # Charger les données de démonstration
            demo_data = load_demo_data()

            # Trouver le télescope et la caméra par leur ID
            telescopes = demo_data.get("telescopes", [])
            cameras = demo_data.get("cameras", [])

            telescope = next(
                (t for t in telescopes if t["id"] == int(telescope_id)), None)
            camera = next(
                (c for c in cameras if c["id"] == int(camera_id)), None)

            if not telescope:
                return JsonResponse({"status": "error", "message": "Télescope non trouvé"}, status=404)
            if not camera:
                return JsonResponse({"status": "error", "message": "Caméra non trouvée"}, status=404)

            # Récupérer les données nécessaires
            focal_length = telescope["focal_length"]  # Longueur focale en mm
            pixel_size = camera["pixel_size"]  # Taille des pixels en microns
            # Largeur du capteur en pixels
            resolution_width = camera["resolution_width"]
            # Hauteur du capteur en pixels
            resolution_height = camera["resolution_height"]

            # Convertir les unités et calculer le champ de vision
            pixel_size_mm = pixel_size / 1000  # Convertir microns en mm
            sensor_width_mm = pixel_size_mm * resolution_width
            sensor_height_mm = pixel_size_mm * resolution_height

            fov_width = (sensor_width_mm / focal_length) * (180 / math.pi)
            fov_height = (sensor_height_mm / focal_length) * (180 / math.pi)

            return JsonResponse({
                "status": "success",
                "data": {"fov_width": fov_width, "fov_height": fov_height}
            })

        except Exception as e:
            return JsonResponse({"status": "error", "message": str(e)}, status=500)
