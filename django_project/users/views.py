from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from .forms import UserRegisterForm, UserUpdateForm, ProfileUpdateForm
from django.contrib.auth.views import LoginView
from django.contrib.auth.forms import AuthenticationForm
import logging

# Set up logger
logger = logging.getLogger(__name__)

# Checking valid email, valid text type, etc. Adding functionality to register page
def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()  # saves the user form
            username = form.cleaned_data.get('username')

            # Log successful registration
            logger.info(f"User '{username}' registered successfully.")

            messages.success(request, f'Your account has been created! You are now able to log in.')
            return redirect('login')
    else:
        form = UserRegisterForm()  # Not valid response? send back to same page
    return render(request, 'users/register.html', {'form': form})

@login_required
def profile(request):
    if request.method == 'POST':
        u_form = UserUpdateForm(request.POST, instance=request.user)
        p_form = ProfileUpdateForm(request.POST,
                                   request.FILES,
                                   instance=request.user.profile)

        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            messages.success(request, 'Your account has been updated!')
            return redirect('profile')

    else:
        u_form = UserUpdateForm(instance=request.user)
        p_form = ProfileUpdateForm(instance=request.user.profile)

    context = {
        'u_form': u_form,
        'p_form': p_form
    }

    return render(request, 'users/profile.html', context)

@login_required
def user_logout(request):
    # Log logout action
    logger.info(f"User '{request.user.username}' logged out successfully.")
    logout(request)
    return render(request, 'users/logout.html', {})

from django.contrib.auth.views import LoginView

def login_view(request):
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.get_user().username if form.get_user() else request.POST.get('username')
            logger.info(f"User '{username}' logged in successfully.")
        else:
            username = request.POST.get("username")
            logger.warning(f"Failed login attempt for username '{username}'.")
    return LoginView.as_view(template_name='users/login.html')(request)