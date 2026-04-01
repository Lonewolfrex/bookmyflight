from django.contrib import admin
from django.urls import path, include
from django.shortcuts import redirect
from flights.views import home, sign_up

def root_view(request):
    """Redirect root to flights home"""
    return redirect('flights:home')

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home, name='home'),              # Root → flights home
    path('sign-up/', sign_up, name='sign_up'), # Global signup
    path('accounts/', include('django.contrib.auth.urls')),
    path('', include('flights.urls')),        # All flights URLs
]
