from django.urls import path
from  alert import views


urlpatterns = [
    path('getalert', views.alert_api),
    # Add other URLs as needed
]
