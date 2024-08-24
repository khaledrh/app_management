from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, update_session_auth_hash
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib import messages
from django.utils.translation import gettext_lazy as _
from apps.models import App
import os


def register_view(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            login(request, form.save())
            messages.success(request, 'Registration successful. Please log in.')
            return redirect('apps:list')
        else:
            messages.error(request, 'Error in registration. Please try again.')
    else:
        form = UserCreationForm()

    return render(request, 'users/register.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            login(request, form.get_user())
            if 'next' in request.POST:
                return redirect(request.POST.get('next'))
            else:
                return redirect('apps:list')  
        else:
            _wrn_msg = 'Incorrect username or password. Please try again.'
            messages.warning(request, _wrn_msg)

    else: 
        form = AuthenticationForm()

    return render(request, 'users/login.html', {'form': form})

def logout_view(request):
    if request.method == 'POST':
        logout(request)
        return redirect('apps:list')

@login_required
def user_settings(request):
    form = PasswordChangeForm(request.user)
    return render(request, 'users/settings.html', {'form': form})

@login_required
def change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  # Important to keep the user logged in
            messages.success(request, 'Your password was successfully updated!')
            return redirect('users:settings')
        else:
            messages.error(request, 'Please correct the error below.')
    else:
        form = PasswordChangeForm(request.user)
    return render(request, 'users/settings.html', {'form': form})

@login_required
def delete_account(request):
    if request.method == 'POST':
        user = request.user
        apps = App.objects.filter(uploaded_by=user)

        # Loop through each app and delete associated APK files
        for app in apps:
            if app.apk_file_path:
                # Ensure the file exists and is a valid file path
                if os.path.isfile(app.apk_file_path.path):
                    # Attempt to delete the file
                    app.apk_file_path.delete(save=False)

            if app.first_screen_screenshot_path:
                if os.path.isfile(app.first_screen_screenshot_path.path):
                    app.first_screen_screenshot_path.delete(save=False)
        
            if app.second_screen_screenshot_path:
                if os.path.isfile(app.second_screen_screenshot_path.path):
                    app.second_screen_screenshot_path.delete(save=False)

            if app.video_recording_path:
                if os.path.isfile(app.video_recording_path.path):
                    app.video_recording_path.delete(save=False)
        user.delete()
        messages.success(request, 'Your account has been deleted.')
        return redirect('apps:list')
    return render(request, 'users/settings.html')
    