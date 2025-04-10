from django.urls import path
from paperInfo import views

urlpatterns = [
    path('info', views.paperInfo),
]
