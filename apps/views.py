from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .appium_script import install_apk_on_emulator, run_appium_test
from django.core.files import File
from .models import App
from .forms import CreateApp
from django.contrib import messages
import os, unicodedata, re, random, string

@login_required(login_url="/users/login/")
def apps_list(request):
    user = request.user

    apps = App.objects.filter(uploaded_by=user).order_by('created_at')
    return render(request, 'apps/app_list.html', {'user': user,'apps': apps})

@login_required(login_url="/users/login/")
def app_page(request, slug):
    app = App.objects.get(slug=slug)

    test_run = (
        app.first_screen_screenshot_path and
        app.second_screen_screenshot_path and
        app.video_recording_path and
        app.ui_hierarchy and
        app.screen_changed is not None  # check if it's not None, as it could be True or False
    )

    return render(request, 'apps/app_page.html', {'app': app, 'test_run': test_run})

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
            # Check if APK file has been updated
            if 'apk_file_path' in form.changed_data:

                # if app.apk_file_path and app.apk_file_path.name:
                #     if app.apk_file_path.path:  # Ensure the path exists
                #         app.apk_file_path.delete(save=False)

                # Reset test result fields
                app.first_screen_screenshot_path = None
                app.second_screen_screenshot_path = None
                app.video_recording_path = None
                app.ui_hierarchy = None
                app.screen_changed = False
            
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

    # Check if the slug is unique
    original_slug = slug
    while App.objects.filter(slug=slug).exists():
        # Generate random characters to append
        random_string = ''.join(random.choices(string.ascii_lowercase + string.digits, k=4))
        slug = f"{original_slug}-{random_string}"
    
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

        # Delete existing files if they exist in both the database and the filesystem
    if app_upload.first_screen_screenshot_path:
        if os.path.isfile(app_upload.first_screen_screenshot_path.path):
            app_upload.first_screen_screenshot_path.delete(save=False)
    
    if app_upload.second_screen_screenshot_path:
        if os.path.isfile(app_upload.second_screen_screenshot_path.path):
            app_upload.second_screen_screenshot_path.delete(save=False)

    if app_upload.video_recording_path:
        if os.path.isfile(app_upload.video_recording_path.path):
            app_upload.video_recording_path.delete(save=False)

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

    # Open the video recording file and save it to the ImageField
    if test_results['video_recording']:
        with open(test_results['video_recording'], 'rb') as f:
            app_upload.video_recording_path.save(
                os.path.basename(test_results['video_recording']),
                File(f),
                save=True
            )

    # app_upload.video_recording_path = test_results['video_recording']
    app_upload.ui_hierarchy = test_results['ui_hierarchy']
    app_upload.screen_changed = test_results['screen_changed']
    
    # Save the changes to the database
    app_upload.save()

    # Redirect back to the app detail page
    return redirect('apps:page', slug=app_upload.slug)