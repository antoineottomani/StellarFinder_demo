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

    def clean_username(self):
        username = self.cleaned_data.get('username')
        if not 6 <= len(username) <= 12:
            raise forms.ValidationError("Le pseudo doit contenir entre 6 et 12 caractères.")
        # username must be composed by letters and number
        if not re.match(r'^[a-zA-Z0-9]+$', username):
            raise forms.ValidationError("Le pseudo ne peut contenir que des lettres et des chiffres.")
        try:
            CustomUser.objects.get(username=username)
            raise forms.ValidationError("Ce pseudo est déjà utilisé.")
        except ObjectDoesNotExist:
            return username

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if email == "":
            raise forms.ValidationError("L'adresse email ne peut pas être vide.")
        try:
            CustomUser.objects.get(email=email)
            raise forms.ValidationError("Cette adresse email est déjà utilisée.")
        except ObjectDoesNotExist:
            return email

    def clean_password1(self):
        password_01 = self.cleaned_data.get('password1')

        if len(password_01) < 8:
            raise forms.ValidationError("Votre mot de passe doit contenir 8 caractères minimum.")
        if not re.search(r'[A-Z]', password_01):
            raise forms.ValidationError("Votre mot de passe doit contenir au moins une lettre majuscule.")
        if not re.search(r'[a-z]', password_01):
            raise forms.ValidationError("Votre mot de passe doit contenir au moins une lettre minuscule.")
        if not re.search(r'[0-9]', password_01):
            raise forms.ValidationError("Votre mot de passe doit contenir au moins un chiffre.")
        if not re.search(r'[\W_]', password_01):
            raise forms.ValidationError("Votre mot de passe doit contenir au moins un caractère spécial.")

        return password_01

    def clean_password2(self):
        password_01 = self.cleaned_data.get('password1')
        password_02 = self.cleaned_data.get('password2')

        # Check if both passwords are identical
        if password_01 and password_02 and password_01 != password_02:
            raise forms.ValidationError("Les mots de passe ne correspondent pas")

        return password_02
