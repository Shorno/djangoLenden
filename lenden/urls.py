from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("create", views.ClientCreateView.as_view(), name="create"),
    path("history", views.history, name="history"),
    path("clients", views.ClientListView.as_view(), name="clients"),
    path("client/<int:pk>", views.ClientDetailView.as_view(), name="client"),
    path("add_payment/<int:client_id>", views.add_payment, name="add_payment"),
    path("client/<int:pk>/update", views.ClientUpdateView.as_view(), name="update"),

]
