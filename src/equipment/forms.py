from django import forms
from .models import Telescope, Camera, StellarObject


class TelescopeForm(forms.ModelForm):
    class Meta:
        model = Telescope
        fields = ['model_name', 'aperture', 'focal_length']

    def clean_aperture(self):
        aperture = self.cleaned_data.get('aperture')
        if aperture is None:
            raise forms.ValidationError("Le champ diamètre est obligatoire.")
        if aperture <= 0:
            raise forms.ValidationError(
                "Le diamètre doit être un nombre positif.")

        return aperture

    def clean_focal_length(self):
        focal_length = self.cleaned_data.get('focal_length')
        if focal_length is None:
            raise forms.ValidationError(
                "Le champ longueur focale est obligatoire.")
        if focal_length <= 0:
            raise forms.ValidationError(
                "La longueur focale doit être un nombre positif.")
        return focal_length


class CameraForm(forms.ModelForm):
    class Meta:
        model = Camera
        fields = ['model_name', 'sensor_type',
                  'resolution_width', 'resolution_height', "pixel_size"]

    def clean(self):
        cleaned_data = super().clean()
        resolution_width = cleaned_data.get("resolution_width")
        resolution_height = cleaned_data.get("resolution_height")
        pixel_size = cleaned_data.get("pixel_size")

        # Vérification que la résolution est dans une plage réaliste
        if resolution_width and resolution_height:
            if resolution_width < 100 or resolution_width > 10000:
                self.add_error(
                    "resolution_width", "La largeur  de l'image doit être comprise entre 100 et 10 000 pixels.")

            if resolution_height < 100 or resolution_height > 10000:
                self.add_error(
                    "resolution_height", "La hauteur de l'image doit être comprise entre 100 et 10 000 pixels.")

        # Vérification que la taille des pixels est réaliste
        if pixel_size:
            if pixel_size < 0.1 or pixel_size > 50:
                self.add_error(
                    "pixel_size", "La taille des pixels doit être comprise entre 0.1 et 50 microns.")

        # Vérification de la taille du capteur en mm
        if resolution_width and resolution_height and pixel_size:
            sensor_width_mm = (pixel_size / 1000) * resolution_width
            sensor_height_mm = (pixel_size / 1000) * resolution_height

            if sensor_width_mm < 5 or sensor_width_mm > 100:
                self.add_error(
                    None, "La largeur du capteur calculée semble anormale (hors plage réaliste : 5-100mm).")

            if sensor_height_mm < 5 or sensor_height_mm > 100:
                self.add_error(
                    None, "La hauteur du capteur calculée semble anormale (hors plage réaliste : 5-100mm).")

        return cleaned_data
