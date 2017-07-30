from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from washeryapp.forms import UserForm, CleanerForm
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User

# Create your views here.
def home(request):
    return redirect(cleaner_home)

@login_required(login_url='/cleaner/sign-in/')
def cleaner_home(request):
    return render(request, 'cleaner/home.html', {})

@login_required(login_url='/cleaner/sign-in/')
def cleaner_account(request):
    return render(request, 'cleaner/account.html', {})

@login_required(login_url='/cleaner/sign-in/')
def cleaner_item(request):
    return render(request, 'cleaner/item.html', {})

@login_required(login_url='/cleaner/sign-in/')
def cleaner_invoice(request):
    return render(request, 'cleaner/invoice.html', {})

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
