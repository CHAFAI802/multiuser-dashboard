from django.shortcuts import render
from django.contrib.auth.decorators import login_required

@login_required
def dashboard_home(request):
    """Tableau de bord personnalisé pour chaque utilisateur connecté."""
    user = request.user  # accès direct à l’utilisateur
    return render(request, "dashboard/dashboard.html", {"user": user})
