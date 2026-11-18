from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth import get_user_model
from django.shortcuts import redirect, render

from .forms import AccountsForm, RegisterForm, UserProfileForm, UserProfileForm


def User_register(request):
    if request.user.is_authenticated:
        return redirect("index")
    if request.method == "POST":
        user_form = RegisterForm(request.POST)
        account_form = AccountsForm(request.POST, request.FILES)
        if user_form.is_valid() and account_form.is_valid():
            user = user_form.save()
            account = account_form.save(commit=False)
            account.user = user
            account.save()
            messages.success(request, "Your account has been created. Please sign in.")
            return redirect("signin")
    else:
        user_form = RegisterForm()
        account_form = AccountsForm()
    return render(request, "register.html", {"user_form": user_form, "account_form": account_form})


def User_login(request):
    if request.user.is_authenticated:
        return redirect("index")
    if request.method == "POST":
        identifier = request.POST.get("email", "").strip()
        password = request.POST.get("password", "")
        User = get_user_model()
        user_record = None
        if "@" in identifier:
            user_record = User.objects.filter(email__iexact=identifier).first()
        else:
            user_record = User.objects.filter(username__iexact=identifier).first()
            if user_record is None:
                matches = Account.objects.filter(phone_number=identifier).select_related("user")
                if matches.count() == 1:
                    user_record = matches.first().user
        user = authenticate(request, username=user_record.get_username(), password=password) if user_record else None
        if user is not None:
            login(request, user)
            messages.success(request, "You are now signed in.")
            return redirect("index")
        messages.error(request, "Invalid username, email, phone number, or password.")
    return render(request, "signin.html")

def User_logout(request):
    if request.method == "POST":
        logout(request)
        messages.success(request, "You have signed out.")
    return redirect("signin")


from django.contrib.auth.decorators import login_required
from .models import Account

@login_required
def User_profile(request):
    account, _ = Account.objects.get_or_create(user=request.user)
    edit_mode = request.GET.get("edit") == "1"
    user_form = UserProfileForm(instance=request.user)
    account_form = AccountsForm(instance=account)
    if request.method == "POST":
        user_form = UserProfileForm(request.POST, instance=request.user)
        account_form = AccountsForm(request.POST, request.FILES, instance=account)
        if user_form.is_valid() and account_form.is_valid():
            user_form.save()
            account_form.save()
            messages.success(request, "Your profile has been updated.")
            return redirect("profile")
        edit_mode = True
    return render(request, "profile.html", {"account": account, "edit_mode": edit_mode, "user_form": user_form, "account_form": account_form})
