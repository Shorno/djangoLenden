from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("create", views.ClientCreateView.as_view(), name="create"),
    path("successful", views.successful, name="successful"),
    path("history", views.history, name="history"),
    path("clients", views.ClientListView.as_view(), name="clients"),
]
