import json
import math
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.urls import reverse_lazy, reverse
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views import View
from django.shortcuts import get_object_or_404
from home.views import load_demo_data


# *Calculate Field Of View (FOV)
# def calculate_fov(focal_length, pixel_size, resolution_width, resolution_height):
#     # Convert pixel size (microns) to mm size
#     pixel_size_mm = pixel_size / 1000

#     # Calculate the physical sensor size in mm
#     sensor_width_mm = pixel_size_mm * resolution_width
#     sensor_height_mm = pixel_size_mm * resolution_height

#     fov_width = (sensor_width_mm / focal_length) * (180 / math.pi)
#     fov_height = (sensor_height_mm / focal_length) * (180 / math.pi)
#     return fov_width, fov_height


def calculate_and_save_fov():

    data_test = load_demo_data()

    for i in data_test:
        print(i)

    # Get the data from the request
    # data = json.loads(request.body)

    return JsonResponse(data_test, status=200)
