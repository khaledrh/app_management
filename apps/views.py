
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .appium_script import  install_apk_on_emulator
from .models import App
from .forms import CreateApp
from django.contrib import messages


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
            slug = f"{newapp.name}-{newapp.uploaded_by}"
            slug = slug.replace(' ', '-')
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


def run_appium_test_view(request, app_id):

    # Retrieve the App object by its ID
    app_upload = get_object_or_404(App, id=app_id)
    
    # Get the path to the uploaded APK file
    apk_path = app_upload.apk_file_path.path

    install_apk_on_emulator(apk_path,"Tradvo")

    # appium_test()
    return render(request, 'apps/app_list.html')
    
    
    # # Define the path where the results will be stored (temporary or permanent)


    # result_path = os.path.join('media', 'tmp_result')
    # # Run the Appium test
    # test_results = run_appium_test(apk_path, result_path)

    # # Save the results back to the App object
    # app_upload.first_screen_screenshot_path = test_results['initial_screenshot']
    # app_upload.second_screen_screenshot_path = test_results['subsequent_screenshot']
    # app_upload.video_recording_path = test_results['video_recording']
    # app_upload.ui_hierarchy = test_results['ui_hierarchy']
    # app_upload.screen_changed = test_results['screen_changed']
    
    # # Save the changes to the database
    # app_upload.save()

    # # Render the results in a template
    # return render(request, 'app_result.html', {'app': app_upload})




# @login_required
# def app_list(request):
#     apps = App.objects.filter(uploaded_by=request.user)
#     return render(request, 'app_list.html', {'apps': apps, 'user': request.user})

# @login_required
# def add_app(request):
#     if request.method == 'POST':
#         form = AppForm(request.POST, request.FILES)
#         if form.is_valid():
#             app = form.save(commit=False)
#             app.uploaded_by = request.user
#             app.save()
#             return JsonResponse({'success': True})
#         else:
#             return JsonResponse({'success': False, 'errors': form.errors})
#     else:
#         form = AppForm()
#     return render(request, 'add_app.html', {'form': form})

# @login_required
# def update_app(request, app_id):
#     app = get_object_or_404(App, id=app_id, uploaded_by=request.user)
#     if request.method == 'POST':
#         form = AppForm(request.POST, request.FILES, instance=app)
#         if form.is_valid():
#             form.save()
#             return redirect('app_list')
#     else:
#         form = AppForm(instance=app)
#     return render(request, 'update_app.html', {'form': form, 'app': app})

# @login_required
# def delete_app(request, app_id):
#     app = get_object_or_404(App, id=app_id, uploaded_by=request.user)
#     if request.method == 'POST':
#         app.delete()
#         return redirect('app_list')
#     return render(request, 'delete_app.html', {'app': app})
#