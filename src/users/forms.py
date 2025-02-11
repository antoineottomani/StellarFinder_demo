import re
from django.core.exceptions import ValidationError, ObjectDoesNotExist
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser
from django import forms


class SignUpForm(UserCreationForm):
    class Meta:
        model = CustomUser
        # Specify the fields we want in the form
        fields = ["username", "email", "password1", "password2"]

    def __init__(self, *args, **kwargs):
        super(SignUpForm, self).__init__(*args, **kwargs)
        self.fields['username'].help_text = "Votre pseudo doit contenir entre 6 et 12 caractères, et ne peut contenir que des lettres et des chiffres."
        self.fields['email'].help_text = "Veuillez entrer une adresse email valide."
        self.fields['password1'].help_text = "Votre mot de passe doit contenir au minimum 8 caractères, au moins une lettre majuscule, une lettre minuscule, un chiffre et un caractère spécial."
        self.fields['password2'].help_text = "Répétez votre mot de passe pour confirmation."
