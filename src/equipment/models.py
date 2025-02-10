from django.db import models
from users.models import CustomUser
from django.core.validators import MinValueValidator, MaxValueValidator


class Telescope(models.Model):
    model_name = models.CharField(max_length=255, verbose_name="Modèle")
    aperture = models.FloatField(verbose_name="Diamètre (mm)", validators=[
                                 MinValueValidator(0.1), MaxValueValidator(1000)])
    focal_length = models.FloatField(verbose_name="Longueur focale (mm)", validators=[
                                     MinValueValidator(50), MaxValueValidator(10000)])
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)

    def __str__(self):
        return self.model_name


class Camera(models.Model):
    SENSOR_TYPES = [
        ("CCD", "CCD"),
        ("CMOS", "CMOS"),
        ("Full-Frame", "Full-Frame"),
        ("APS-C", "APS-C"),
        ("Micro 4/3", "Micro 4/3"),
    ]
    model_name = models.CharField(max_length=255, verbose_name="Modèle")
    sensor_type = models.CharField(
        max_length=255, verbose_name="Type de capteur", choices=SENSOR_TYPES)
    resolution_width = models.IntegerField(verbose_name="Résolution (largeur)",  validators=[
                                           MinValueValidator(100), MaxValueValidator(10000)])
    resolution_height = models.IntegerField(verbose_name="Résolution (hauteur)",  validators=[
                                            MinValueValidator(100), MaxValueValidator(10000)])
    pixel_size = models.FloatField(verbose_name="Taille des pixels (micron)",  validators=[
                                   MinValueValidator(0.1), MaxValueValidator(50)])
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)

    def __str__(self):
        return self.model_name


class StellarObject(models.Model):
    name = models.CharField(max_length=255, verbose_name="Nom")
    catalog_name = models.CharField(max_length=255, verbose_name="Catalogue")
    declination = models.FloatField(verbose_name="Déclinaison (degrés)")
    right_ascension = models.FloatField(
        verbose_name="Ascension droite (degrés)")
    constellation = models.CharField(
        max_length=255, verbose_name="Constellation")
    meridien = models.DateTimeField(verbose_name="Passage au méridien")
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class Framing(models.Model):
    field_of_view = models.CharField(
        max_length=255, verbose_name="FOV (degrés)")
    telescope = models.ForeignKey(Telescope, on_delete=models.CASCADE)
    camera = models.ForeignKey(Camera, on_delete=models.CASCADE)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    stellar_object = models.ForeignKey(StellarObject, on_delete=models.CASCADE)

    def __str__(self):
        return f"Cadrage de {self.stellar_object.name} par {self.user.username}"
