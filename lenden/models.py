from django.db import models


# Create your models here.
class Client(models.Model):
    name = models.CharField(max_length=200)
    email = models.EmailField()
    phone = models.CharField(max_length=20)
    created = models.DateField(auto_now_add=True)
    loan_amount = models.IntegerField()
    paid_amount = models.IntegerField(default=0)

    def remaining(self):
        return self.loan_amount - self.paid_amount

    def __str__(self):
        return self.name


class PaymentHistory(models.Model):
    client = models.ForeignKey(Client, on_delete=models.CASCADE)
    payment_date = models.DateTimeField(auto_now_add=True)
    payment_amount = models.IntegerField()