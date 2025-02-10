from django.shortcuts import redirect


class RestrictDemoActionsMixin:
    def dispatch(self, request, *args, **kwargs):
        # Si on est en mode démo, redirige vers la page démo
        if request.path.startswith("/demo/"):  # Ou vérifie un autre critère
            return redirect("compte-demo")
        return super().dispatch(request, *args, **kwargs)
