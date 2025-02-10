from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView
from .models import CustomUser
from .forms import SignUpForm
from django.views.generic import CreateView, TemplateView
from django.shortcuts import redirect
from django.conf import settings
import pathlib
import json


class SignUpView(CreateView):
    model = CustomUser
    form_class = SignUpForm
    template_name = "users/signup.html"
    success_url = reverse_lazy("connexion")

    def get_context_data(self, **kwargs):
        # Ajout de l'indicateur 'is_demo' dans le contexte
        context = super().get_context_data(**kwargs)
        context["is_demo"] = settings.DEMO_MODE
        return context


class DemoLoginView(LoginView):
    template_name = "users/login.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['is_demo'] = settings.DEMO_MODE
        return context


def load_demo_data():
    with open(settings.DEMO_DATA_PATH, "r") as file:
        return json.load(file)


class DemoAccountView(TemplateView):
    template_name = "users/demo_account.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # Load static data for demo account
        demo_data = load_demo_data()
        context["telescopes"] = demo_data.get("telescopes")
        context["cameras"] = demo_data.get("cameras")

        # Indicateur du mode démo
        context["is_demo"] = True
        return context
