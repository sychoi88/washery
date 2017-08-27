from django import forms

from django.contrib.auth.models import User
from washeryapp.models import Cleaner, Item, Invoice, InvoiceDetail

from django.forms import BaseFormSet


class UserForm(forms.ModelForm):
    email = forms.CharField(max_length=100, required=True)
    password = forms.CharField(widget=forms.PasswordInput())

    class Meta:
        model = User
        fields = ("username", "password", "first_name", "last_name", "email")

class UserFormForEdit(forms.ModelForm):
    email = forms.CharField(max_length=100, required=True)

    class Meta:
        model = User
        fields = ("first_name", "last_name", "email")

class CleanerForm(forms.ModelForm):
    class Meta:
        model = Cleaner
        fields = ("name", "phone", "address", "logo")

class ItemForm(forms.ModelForm):
    class Meta:
        model = Item
        exclude = ("cleaner",)

class InvoiceForm(forms.ModelForm):
    class Meta:
        model = Invoice
        exclude = ("cleaner",)

class CreateInvoiceForm(forms.ModelForm):
    address = forms.CharField(max_length=100, required=True)

    class Meta:
        model = Invoice
        fields = ("customer", "address")

class BaseInvoiceDetailFormSet(BaseFormSet):
    def clean(self):
        """Check that there is at least 1"""
        if(any(self.errors)):
            # Don't bother validating the formset unless each form is valid on its own
            return
        if len(self.forms) < 1:
            raise forms.ValidationError("Must have at least one invoiceDetail.")
        items = []
        for form in self.forms:
            item = form.cleaned_data['item']
            if item in items:
                raise forms.ValidationError("duplicate " + str(item))
            items.append(item)


class InvoiceDetailForm(forms.ModelForm):
    quantity = forms.IntegerField(initial=1, required=True)
    class Meta:
        model = InvoiceDetail
        fields = ("item", "quantity")
