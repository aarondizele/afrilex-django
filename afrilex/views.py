from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from application.models import Practice, Firm, Office, Expert
from application.forms import ExpertForm, CreateUserForm
from application.decorators import unauthenticated_user, allowed_users

def home_view(request):

    context = {"title": "Afrilex"}

    return render(request, 'home.html', context)


def about_view(request):

    context = {"title": "A propos d'Afrilex"}

    return render(request, 'about.html', context)


def office_view(request, slug):

    obj = get_object_or_404(Office, slug=slug)

    context = {"object": obj}

    return render(request, 'office.html', context)


def expert_view(request, slug):

    obj = get_object_or_404(Expert, slug=slug)

    context = {"object": obj}

    return render(request, 'expert.html', context)


@login_required(login_url='login')
def add_profile_view(request):
    form = ExpertForm(request.POST or None)
    if form.is_valid():
        obj = form.save(commit=False)
        obj.user = request.user
        obj.save()

        form = ExpertForm()
        return redirect('home')

    context = {"form": form}
    return render(request, 'add-profile.html', context)



@login_required(login_url='login')
def delete_expert_view(request, slug):
    obj = get_object_or_404(Expert, slug=slug)
    if request.method == 'POST':
        obj.delete()
        return redirect("home")

    context = {"object": obj}
    return render(request, "delete.html", context)

@unauthenticated_user
def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username', None)
        password = request.POST.get('password', None)

        user = authenticate(username=username, password=password)

        if user is not None:
            login(request, user)

            return redirect("home")
        else:
            messages.add_message(request, messages.ERROR, "Aucun utilisateur avec ce nom d'utilisateur ou mot de passe. Veuillez réessayer")

    context = {"title": "Se connecter"}

    return render(request, 'login.html', context)

@unauthenticated_user
def signup_view(request):
    if request.method == 'POST':
        form = CreateUserForm(request.POST)
        
        if form.is_valid():
            form.save()
            
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')

            messages.add_message(request,messages.SUCCESS, 'Account was created for ' + username)

            user = authenticate(username=username, password=raw_password)
            login(request, user)

            return redirect("home")

    else:

        form = CreateUserForm()

    context = {"form": form}
    
    return render(request, 'signup.html', context)


@login_required(login_url='login')
def edit_profile_view(request, slug):
    obj = get_object_or_404(Expert, slug=slug)
    form = ExpertForm(request.POST or None, instance=obj)
    if form.is_valid():
        form.save()

    context = {"title": f"Mettre à jour votre profil"}
    return render(request, 'edit-profile.html', context)


@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def notifications_view(request):

    context = {"title": "Mes notifications"}

    return render(request, 'notifications.html', context)


@login_required(login_url='login')
def account_view(request):

    context = {"title": "Mon compte"}

    return render(request, 'account.html', context)


def logout_view(request):
    if not request.user.is_authenticated:
        return redirect('home')

    logout(request)

    return redirect('login')