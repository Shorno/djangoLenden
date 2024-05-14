from django.db.models import Sum
from django.shortcuts import render, get_object_or_404, redirect
from .models import Client
from django.views.generic.edit import CreateView
from django.views.generic.list import ListView
from django.views.generic import DetailView
from .forms import CreateClientForm, PaymentForm


# Create your views here.

class ClientCreateView(CreateView):
    model = Client
    form_class = CreateClientForm
    template_name = "client_form.html"
    success_url = "/clients"


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


def history(request):
    clients = Client.objects.all()

    return render(request, "history.html", {
        "clients": clients,
    })


class ClientListView(ListView):
    model = Client
    template_name = "clients_list.html"
    context_object_name = "clients"
    ordering = ["name"]
    paginate_by = 20


class ClientDetailView(DetailView):
    model = Client
    template_name = "client_detail.html"
    context_object_name = "client"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['total_paid'] = self.object.paid_amount
        context['total_remaining'] = self.object.loan_amount - self.object.paid_amount
        return context


def add_payment(request, client_id):
    client = get_object_or_404(Client, id=client_id)
    if request.method == 'POST':
        form = PaymentForm(request.POST)
        if form.is_valid():
            payment_amount = form.cleaned_data['payment_amount']
            client.paid_amount += payment_amount
            client.save()
            return redirect('client', pk=client.id)
    else:
        form = PaymentForm()
    return render(request, 'add_payment.html', {'form': form, 'client': client})
