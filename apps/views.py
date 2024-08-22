
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .appium_script import install_apk_on_emulator, run_appium_test
from django.core.files import File
from .models import App
from .forms import CreateApp
from django.contrib import messages
import os
import unicodedata
import re

@login_required(login_url="/users/login/")
def apps_list(request):
    user = request.user

    apps = App.objects.filter(uploaded_by=user).order_by('created_at')
    return render(request, 'apps/app_list.html', {'user': user,'apps': apps})

@login_required(login_url="/users/login/")
def app_page(request, slug):
    apps = App.objects.get(slug=slug)
    return render(request, 'apps/app_page.html', {'app': apps})

@login_required(login_url="/users/login/")
def app_new(request):
    if request.method == 'POST':
        form = CreateApp(request.POST, request.FILES)
        if form.is_valid():
            newapp = form.save(commit=False)
            newapp.uploaded_by = request.user
            slug = create_slug(newapp.name, newapp.uploaded_by)
            newapp.slug = slug
            newapp.save()
            return redirect('apps:list')
    else:
        form = CreateApp()
    form = CreateApp()
    return render(request, 'apps/app_new.html', {'form': form})

@login_required(login_url="/users/login/")
def app_update(request, slug):
    app = get_object_or_404(App, slug=slug)
    
    if request.user != app.uploaded_by:
        messages.error(request, "You are not authorized to edit this app.")
        return redirect('apps:page', slug=slug)

    if request.method == 'POST':
        form = CreateApp(request.POST, request.FILES, instance=app)
        if form.is_valid():
            form.save()
            return redirect('apps:page', slug=slug)
    else:
        form = CreateApp(instance=app)
    
    return render(request, 'apps/app_edit.html', {'form': form, 'app': app})

@login_required(login_url="/users/login/")
def app_delete(request, slug):
    app = get_object_or_404(App, slug=slug)
    
    if request.user != app.uploaded_by:
        messages.error(request, "You are not authorized to delete this app.")
        return redirect('apps:page', slug=slug)
    
    if request.method == 'POST':
        app.delete()
        return redirect('apps:list')
    
    return render(request, 'apps/app_confirm_delete.html', {'app': app})


def create_slug(name, uploaded_by):
    # Combine the name and uploaded_by fields
    slug = f"{name}-{uploaded_by}"
    
    # Normalize the string to NFKD (decompose accented characters)
    slug = unicodedata.normalize('NFKD', slug)
    
    # Convert to lowercase
    slug = slug.lower()
    
    # Replace non-ASCII characters with their closest ASCII equivalent
    slug = slug.encode('ascii', 'ignore').decode('ascii')
    
    # Replace spaces with hyphens
    slug = slug.replace(' ', '-')
    
    # Remove any remaining special characters (anything that is not a letter, number, or hyphen)
    slug = re.sub(r'[^a-z0-9-]+', '', slug)
    
    # Replace multiple hyphens with a single hyphen
    slug = re.sub(r'-+', '-', slug)
    
    # Remove leading or trailing hyphens
    slug = slug.strip('-')
    
    return slug

def run_appium_test_view(request, app_id):

    # Retrieve the App object by its ID
    app_upload = get_object_or_404(App, id=app_id)
    
    # Get the path to the uploaded APK file
    apk_path = app_upload.apk_file_path.path

    install_apk_on_emulator(apk_path,"Tradvo")

    # Define the path where the results will be stored (temporary or permanent)
    result_path = os.path.join('media', 'tmp_result')
    # Run the Appium test
    test_results = run_appium_test(apk_path, result_path)


    # Save the results back to the App object
    # Open the initial screenshot file and save it to the ImageField
    if test_results['initial_screenshot']:
        with open(test_results['initial_screenshot'], 'rb') as f:
            app_upload.first_screen_screenshot_path.save(
                os.path.basename(test_results['initial_screenshot']),
                File(f),
                save=True
            )

    # Open the subsequent screenshot file and save it to the ImageField
    if test_results['subsequent_screenshot']:
        with open(test_results['subsequent_screenshot'], 'rb') as f:
            app_upload.second_screen_screenshot_path.save(
                os.path.basename(test_results['subsequent_screenshot']),
                File(f),
                save=True
            )
    # app_upload.video_recording_path = test_results['video_recording']
    app_upload.ui_hierarchy = test_results['ui_hierarchy']
    app_upload.screen_changed = test_results['screen_changed']
    
    # Save the changes to the database
    app_upload.save()

    # # Render the results in a template
    # return render(request, 'app_result.html', {'app': app_upload})
    return render(request, 'apps/app_list.html')