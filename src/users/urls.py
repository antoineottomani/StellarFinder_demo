from django.urls import path
from .views import SignUpView, DemoAccountView, DemoLoginView


urlpatterns = [
    path('compte-demo/', DemoAccountView.as_view(), name="compte-demo"),
    path('inscription/', SignUpView.as_view(), name="inscription"),
    path('connexion/', DemoLoginView.as_view(), name="connexion"),
]
