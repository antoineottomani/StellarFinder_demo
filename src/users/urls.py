from django.urls import path, include
from .views import SignUpView, UserAccountView, logout_view, DemoAccountView, DemoLoginView
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('compte/', UserAccountView.as_view(), name="mon-compte"),
    path('demo/', DemoAccountView.as_view(), name="compte-demo"),
    path('inscription/', SignUpView.as_view(), name="inscription"),
    # path('connexion/', auth_views.LoginView.as_view(template_name="users/login.html"), name="connexion"),
    path('connexion/', DemoLoginView.as_view(), name="connexion"),
    path('deconnexion/', logout_view, name="deconnexion"),
]
