# predictor/urls.py — URL routes for the predictor app

from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),           # Home page with prediction form
    path('health/', views.health, name='health'), # Optional health check endpoint
]