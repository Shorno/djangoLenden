from django import forms
from .models import Client


class CreateClientForm(forms.ModelForm):
    class Meta:
        model = Client
        fields = "__all__"
        labels = {
            "name": "Name",
            "email": "Email",
            "phone": "Phone",
            "loan_amount": "Loan Amount",
            "paid_amount": "Paid Amount"
        }
        error_messages = {
            "name": {
                "required": "Please enter client name"
            },
            "email": {
                "required": "Please enter client email"
            },
            "phone": {
                "required": "Please enter client phone number"
            },
            "loan_amount": {
                "required": "Please enter the loan amount"
            },
            "paid_amount": {
                "required": "Please enter the paid amount"
            }
        }
