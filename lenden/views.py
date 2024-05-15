from django.contrib.auth.decorators import login_required
from django.db.models import Sum
from django.shortcuts import render, get_object_or_404, redirect
from .models import Client, PaymentHistory
from django.views.generic.edit import CreateView, UpdateView
from django.views.generic.list import ListView
from django.views.generic import DetailView
from .forms import CreateClientForm, PaymentForm
from django.urls import reverse


# Create your views here.

class ClientCreateView(CreateView):
    model = Client
    form_class = CreateClientForm
    template_name = "client_form.html"

    def get_success_url(self):
        return reverse('client', kwargs={'pk': self.object.id})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["form_type"] = "Create"
        return context


@login_required
def index(request):
    total = Client.objects.count()
    total_loan_amount = Client.objects.aggregate(Sum("loan_amount"))["loan_amount__sum"]
    total_got_paid = Client.objects.aggregate(Sum("paid_amount"))["paid_amount__sum"]
    # remaining = total_loan_amount - total_got_paid
    remaining = max(0, total_loan_amount - total_got_paid)
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

    # def get_context_data(self, **kwargs):
    #     context = super().get_context_data(**kwargs)
    #     context['total_paid'] = self.object.paid_amount
    #     context['total_remaining'] = self.object.loan_amount - self.object.paid_amount
    #     context['payment_history'] = self.object.paymenthistory_set.all().order_by('-payment_date')
    #     return context

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['total_paid'] = self.object.paid_amount
        context['total_remaining'] = self.object.loan_amount - self.object.paid_amount
        payment_history = self.object.paymenthistory_set.all().order_by('-payment_date')
        context['payment_history'] = payment_history
        context['last_payment_date'] = payment_history[0].payment_date if payment_history else None
        return context


def add_payment(request, client_id):
    client = get_object_or_404(Client, id=client_id)
    if request.method == 'POST':
        form = PaymentForm(request.POST)
        if form.is_valid():
            payment_amount = form.cleaned_data['payment_amount']
            client.paid_amount += payment_amount
            client.save()
            PaymentHistory.objects.create(client=client, payment_amount=payment_amount)

            return redirect('client', pk=client.id)
    else:
        form = PaymentForm()
    return render(request, 'add_payment.html', {'form': form, 'client': client})


class ClientUpdateView(UpdateView):
    model = Client
    form_class = CreateClientForm
    template_name = "client_form.html"

    def get_success_url(self):
        return reverse('client', kwargs={'pk': self.object.id})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["form_type"] = "Update"
        return context
