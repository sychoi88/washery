from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required

from washeryapp.forms import (UserForm, CleanerForm, UserFormForEdit, ItemForm, InvoiceForm,
                                CreateInvoiceForm, BaseInvoiceDetailFormSet)
from django.contrib.auth import authenticate, login

from django.contrib.auth.models import User
from washeryapp.models import Item, Invoice, InvoiceDetail

from django.forms import inlineformset_factory, modelformset_factory

# Create your views here.
def home(request):
    return redirect(cleaner_home)

@login_required(login_url='/cleaner/sign-in/')
def cleaner_home(request):
    return redirect(cleaner_invoice)

@login_required(login_url='/cleaner/sign-in/')
def cleaner_account(request):
    user_form = UserFormForEdit(instance = request.user)
    cleaner_form = CleanerForm(instance = request.user.cleaner)

    if request.method == "POST":
        user_form = UserFormForEdit(request.POST, instance=request.user)
        cleaner_form = CleanerForm(request.POST, request.FILES, instance = request.user.cleaner)

        if user_form.is_valid() and cleaner_form.is_valid():
            user_form.save()
            cleaner_form.save()

    return render(request, 'cleaner/account.html', {
        "user_form": user_form,
        "cleaner_form": cleaner_form
    })

@login_required(login_url='/cleaner/sign-in/')
def cleaner_item(request):
    items = Item.objects.filter(cleaner=request.user.cleaner).order_by("-id")
    return render(request, 'cleaner/item.html', {"items": items})

@login_required(login_url='/cleaner/sign-in/')
def cleaner_add_item(request):
    form = ItemForm()

    if request.method == "POST":
        form = ItemForm(request.POST, request.FILES)

        if form.is_valid():
            item = form.save(commit=False)
            item.cleaner = request.user.cleaner
            item.save()
            return redirect(cleaner_item)

    return render(request, 'cleaner/add_item.html', {
        "form": form
    })

@login_required(login_url='/cleaner/sign-in/')
def cleaner_edit_item(request, item_id):
    form = ItemForm(instance = Item.objects.get(id= item_id))

    if request.method == "POST":
        form = ItemForm(request.POST, request.FILES, instance = Item.objects.get(id = item_id))

        if form.is_valid():
            form.save()
            return redirect(cleaner_item)

    return render(request, 'cleaner/edit_item.html', {
        "form": form
    })

# INVOICE
@login_required(login_url='/cleaner/sign-in/')
def cleaner_invoice(request):

    if request.method == "POST":
        invoice = Invoice.objects.get(id = request.POST["id"], cleaner = request.user.cleaner)

        if invoice.status == Invoice.CLEANING:
            invoice.status = Invoice.READY
            invoice.save()

    invoices = Invoice.objects.filter(cleaner = request.user.cleaner).order_by("-id")
    return render(request, 'cleaner/invoice.html', {"invoices":invoices})



@login_required(login_url='/cleaner/sign-in/')
def cleaner_add_invoice(request):
    invoice_form = CreateInvoiceForm(prefix="invoice")

    InvoiceDetailFormSet = modelformset_factory(InvoiceDetail, fields=('item', 'quantity'),
                                formset=BaseInvoiceDetailFormSet,
                                can_delete = False, extra = 0, min_num=1)
    invoiceDetail_formset = InvoiceDetailFormSet(prefix="line")

    if request.method == "POST":
        invoice_form = CreateInvoiceForm(request.POST, request.FILES, prefix="invoice")
        invoiceDetail_formset = InvoiceDetailFormSet(request.POST, prefix="line")

        #save form here.
        if invoice_form.is_valid() and invoiceDetail_formset.is_valid():
            try:
                invoice = invoice_form.save(commit=False)

                total = 0
                for idet in invoiceDetail_formset:
                    detail = idet.save(commit=False)
                    detail.sub_total = detail.quantity * detail.item.price
                    total += detail.sub_total

                invoice.cleaner = request.user.cleaner
                invoice.status = Invoice.CLEANING
                invoice.total = total  # Set the calculated total.
                invoice.save()

                for idet in invoiceDetail_formset:
                    detail = idet.save(commit=False)
                    detail.invoice = invoice
                    detail.save()


            except Exception as e:
                print("################# ERROR SAVING TO DB: " + str(e))

            return redirect(cleaner_home)

    return render(request, 'cleaner/add_invoice.html', {
        "invoice_form": invoice_form,
        "invoiceDetail_formset": invoiceDetail_formset,
    })

# @login_required(login_url='/cleaner/sign-in/')
# def cleaner_route(request):
#     return render(request, 'cleaner/route.html', {})
#
# # needs the route id.
# @login_required(login_url='/cleaner/sign-in/')
# def cleaner_stop(request):
#     return render(request, 'cleaner/stop.html', {})



@login_required(login_url='/cleaner/sign-in/')
def cleaner_report(request):
    return render(request, 'cleaner/report.html', {})

def cleaner_sign_up(request):
    user_form = UserForm()
    cleaner_form = CleanerForm()

    if request.method == "POST":
        user_form = UserForm(request.POST)
        cleaner_form = CleanerForm(request.POST, request.FILES)

        if user_form.is_valid() and cleaner_form.is_valid():
            new_user = User.objects.create_user(**user_form.cleaned_data)
            new_cleaner = cleaner_form.save(commit = False)
            new_cleaner.user = new_user
            new_cleaner.save()

            login(request,authenticate(
                username = user_form.cleaned_data["username"],
                password = user_form.cleaned_data["password"]
            ))

            return redirect(cleaner_home)

    return render(request, 'cleaner/sign_up.html', {
        "user_form": user_form,
        "cleaner_form": cleaner_form
    })
