# diabetes_project/urls.py — Root URL configuration

from django.urls import path, include

urlpatterns = [
    path('', include('predictor.urls')),  # Delegate all routes to the predictor app
]