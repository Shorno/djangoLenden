from django.db.models import Sum
from django.shortcuts import render
from .models import Client
from django.views.generic.edit import CreateView
from django.views.generic.list import ListView
from .forms import CreateClientForm


# Create your views here.

class ClientCreateView(CreateView):
    model = Client
    form_class = CreateClientForm
    template_name = "client_form.html"
    success_url = "/successful"


def index(request):
    total = Client.objects.count()
    total_loan_amount = Client.objects.aggregate(Sum("loan_amount"))["loan_amount__sum"]
    total_got_paid = Client.objects.aggregate(Sum("paid_amount"))["paid_amount__sum"]
    remaining = total_loan_amount - total_got_paid
    return render(request, 'index.html', {
        "total": total,
        "total_loan_amount": total_loan_amount,
        "total_got_paid": total_got_paid,
        "remaining": remaining,
    })


def successful(request):
    return render(request, "successful.html")


def history(request):
    clients = Client.objects.all()

    return render(request, "history.html", {
        "clients": clients,
    })


class ClientListView(ListView):
    model = Client
    template_name = "clients_list.html"
    context_object_name = "clients"
    ordering = ["-name"]
    paginate_by = 2



