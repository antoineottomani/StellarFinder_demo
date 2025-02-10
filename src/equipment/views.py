import json
import math
from .models import Telescope, Camera, Framing, StellarObject
from .forms import TelescopeForm, CameraForm
from django.views.generic import CreateView, ListView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.urls import reverse_lazy, reverse
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views import View
from django.shortcuts import get_object_or_404
from .mixins import RestrictDemoActionsMixin


# *CRUD Telescope
class ListTelescope(RestrictDemoActionsMixin, LoginRequiredMixin, ListView):
    model = Telescope
    context_object_name = "telescopes"
    template_name = "equipment/telescope_list.html"


class CreateTelescope(RestrictDemoActionsMixin, LoginRequiredMixin, CreateView):
    model = Telescope
    form_class = TelescopeForm
    template_name = "equipment/telescope_form.html"
    success_url = reverse_lazy("mon-compte")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['action'] = reverse('ajouter-telescope')
        context['submit_text'] = 'Enregistrer'
        return context

    # Lorsque le form d'ajout de télescope est valide
    def form_valid(self, form):
        form.instance.user = self.request.user
        response = super().form_valid(form)

        # Si la requête est une requête AJAX
        if self.request.headers.get('x-requested-with') == 'XMLHttpRequest':
            return JsonResponse({'success': True})

        return response

    # Lorsque le form d'ajout de télescope est invalide
    def form_invalid(self, form):

        # Si la requête est une requête AJAX
        if self.request.headers.get('x-requested-with') == 'XMLHttpRequest':
            errors = form.errors.get_json_data()

            # Retourner une réponse JSON avec les erreurs de validation
            return JsonResponse({'success': False, 'errors': errors}, status=400)

        # Si la requête n'est pas une requête AJAX
        return super().form_invalid(form)


class UpdateTelescope(RestrictDemoActionsMixin, LoginRequiredMixin, UpdateView):
    model = Telescope
    form_class = TelescopeForm
    template_name = "equipment/telescope_form.html"
    success_url = reverse_lazy("mon-compte")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['action'] = reverse(
            'modifier-telescope', kwargs={'pk': self.object.pk})
        context['submit_text'] = 'Modifier'
        return context

    # Lorsque le form de modification de télescope est valide
    def form_valid(self, form):
        form.instance.user = self.request.user
        response = super().form_valid(form)

        # Si la requête est une requête AJAX
        if self.request.headers.get('x-requested-with') == 'XMLHttpRequest':
            return JsonResponse({'success': True})

        return response

    # Lorsque le form de modification de télescope est invalide
    def form_invalid(self, form):

        # Si la requête est une requête AJAX :
        if self.request.headers.get('x-requested-with') == 'XMLHttpRequest':
            errors = form.errors.get_json_data()

            # Retourner une réponse JSON avec les erreurs de validation
            return JsonResponse({'success': False, 'errors': errors}, status=400)

        # Si la requête n'est pas une requête AJAX
        return super().form_invalid(form)


class DeleteTelescope(RestrictDemoActionsMixin, LoginRequiredMixin, DeleteView):
    model = Telescope
    template_name = "equipment/telescope_delete.html"
    success_url = reverse_lazy("mon-compte")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['action'] = reverse(
            'supprimer-telescope', kwargs={'pk': self.object.pk})
        context['submit_text'] = 'Supprimer'
        return context

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()

        # Si la requête est une requête AJAX
        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            self.object.delete()
            return JsonResponse({'success': True})

        return super().delete(request, *args, **kwargs)


# *CRUD Camera
class ListCamera(LoginRequiredMixin, ListView):
    model = Camera
    context_object_name = "cameras"
    template_name = "equipment/camera_list.html"


class CreateCamera(RestrictDemoActionsMixin, LoginRequiredMixin, CreateView):
    model = Camera
    form_class = CameraForm
    template_name = "equipment/camera_form.html"
    success_url = reverse_lazy("mon-compte")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['action'] = reverse_lazy('ajouter-camera')
        context['submit_text'] = 'Enregistrer'
        return context

    # Lorsque le form d'ajout de camera est valide
    def form_valid(self, form):
        form.instance.user = self.request.user
        response = super().form_valid(form)

        # Si la requête est une requête AJAX
        if self.request.headers.get('x-requested-with') == 'XMLHttpRequest':
            return JsonResponse({'success': True})

        return response

    # Lorsque le form d'ajout de camera est invalide
    def form_invalid(self, form):

        # Si la requête est une requête AJAX
        if self.request.headers.get('x-requested-with') == 'XMLHttpRequest':
            errors = form.errors.get_json_data()

            # Retourner une réponse JSON avec les erreurs de validation
            return JsonResponse({'success': False, 'errors': errors}, status=400)

        # Si la requête n'est pas une requête AJAX
        return super().form_invalid(form)


class UpdateCamera(RestrictDemoActionsMixin, LoginRequiredMixin, UpdateView):
    model = Camera
    form_class = CameraForm
    template_name = "equipment/camera_form.html"
    success_url = reverse_lazy('mon-compte')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['action'] = reverse(
            'modifier-camera', kwargs={'pk': self.object.pk})
        context['submit_text'] = 'Modifier'
        return context

    # Lorsque le form de modification de camera est valide
    def form_valid(self, form):
        form.instance.user = self.request.user
        response = super().form_valid(form)

        # Si la requête est une requête AJAX
        if self.request.headers.get('x-requested-with') == 'XMLHttpRequest':
            return JsonResponse({'success': True})

        return response

    # Lorsque le form de modification de camera est invalide
    def form_invalid(self, form):

        # Si la requête est une requête AJAX
        if self.request.headers.get('x-requested-with') == 'XMLHttpRequest':
            errors = form.errors.get_json_data()

            # Retourner une réponse JSON avec les erreurs de validation
            return JsonResponse({'success': False, 'errors': errors}, status=400)

        # Si la requête n'est pas une requête AJAX
        return super().form_invalid(form)


class DeleteCamera(RestrictDemoActionsMixin, LoginRequiredMixin, DeleteView):
    model = Camera
    template_name = "equipment/camera_delete.html"
    success_url = reverse_lazy('mon-compte')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['action'] = reverse(
            'supprimer-camera', kwargs={'pk': self.object.pk})
        context['submit_text'] = 'Supprimer'
        return context

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()

        # Si la requête est une requête AJAX
        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            self.object.delete()
            return JsonResponse({'success': True})

        return super().delete(request, *args, **kwargs)


# *Calculate Field Of View (FOV)
def calculate_fov(focal_length, pixel_size, resolution_width, resolution_height):
    # Convert pixel size (microns) to mm size
    pixel_size_mm = pixel_size / 1000

    # Calculate the physical sensor size in mm
    sensor_width_mm = pixel_size_mm * resolution_width
    sensor_height_mm = pixel_size_mm * resolution_height

    fov_width = (sensor_width_mm / focal_length) * (180 / math.pi)
    fov_height = (sensor_height_mm / focal_length) * (180 / math.pi)
    return fov_width, fov_height


@login_required
def calculate_and_save_fov(request, telescope_id, camera_id):
    try:
        telescope = get_object_or_404(
            Telescope, id=telescope_id, user=request.user)
        camera = get_object_or_404(Camera, id=camera_id, user=request.user)

        # Get parameters for FOV calculation
        fov_width, fov_height = calculate_fov(
            telescope.focal_length, camera.pixel_size, camera.resolution_width, camera.resolution_height)

        fov_width = round(fov_width, 2)
        fov_height = round(fov_height, 2)

        return JsonResponse({
            'status': 'success',
            'data': {
                'fov_width': fov_width,
                'fov_height': fov_height
            }
        })

    except Exception as e:
        return JsonResponse({'error': str(e)}, status=400)


@method_decorator(csrf_exempt, name='dispatch')
class SaveFramingView(LoginRequiredMixin, View):
    def post(self, request, *args, **kwargs):
        try:
            data = json.loads(request.body)

            # Validate required fields
            required_fields = ['name', 'catalog_name', 'right_ascension', 'declination',
                               'constellation', 'meridien', 'telescope', 'camera', 'fov_width', 'fov_height']
            for field in required_fields:
                if field not in data:
                    return JsonResponse({'status': 'error', 'message': f"Le champ requis {field} est manquant"}, status=400)

            # Stellar Object attributes
            name = data['name']
            catalog_name = data['catalog_name']
            right_ascension = data['right_ascension']
            declination = data['declination']
            constellation = data['constellation']
            meridien = data['meridien']

            # Framing attributes
            telescope_id = data['telescope']
            camera_id = data['camera']
            fov_width = data['fov_width']
            fov_height = data['fov_height']
            field_of_view = f"{fov_width} x {fov_height}"

            # Get the telescope and camera objects
            telescope = get_object_or_404(
                Telescope, id=telescope_id, user=request.user)
            camera = get_object_or_404(Camera, id=camera_id, user=request.user)

            # Save or update the stellar object
            stellar_object, created = StellarObject.objects.get_or_create(
                name=name,
                defaults={
                    'catalog_name': catalog_name,
                    'right_ascension': right_ascension,
                    'declination': declination,
                    'constellation': constellation,
                    'meridien': meridien
                }
            )

            if not created:
                # If the object already exists, update its informations
                stellar_object.catalog_name = catalog_name
                stellar_object.right_ascension = right_ascension
                stellar_object.declination = declination
                stellar_object.constellation = constellation
                stellar_object.meridien = meridien
                stellar_object.save()

            # Save the framing
            framing = Framing.objects.create(
                user=request.user,
                telescope=telescope,
                camera=camera,
                stellar_object=stellar_object,
                field_of_view=field_of_view
            )

            return JsonResponse({'status': 'success', 'message': 'Cadrage correctement enregistré.'})

        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)})
