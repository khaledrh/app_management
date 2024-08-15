
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from .models import App
from .forms import AppForm

@login_required
def app_list(request):
    apps = App.objects.filter(uploaded_by=request.user)
    return render(request, 'app_list.html', {'apps': apps, 'user': request.user})

@login_required
def add_app(request):
    if request.method == 'POST':
        form = AppForm(request.POST, request.FILES)
        if form.is_valid():
            app = form.save(commit=False)
            app.uploaded_by = request.user
            app.save()
            return JsonResponse({'success': True})
        else:
            return JsonResponse({'success': False, 'errors': form.errors})
    else:
        form = AppForm()
    return render(request, 'add_app.html', {'form': form})

@login_required
def update_app(request, app_id):
    app = get_object_or_404(App, id=app_id, uploaded_by=request.user)
    if request.method == 'POST':
        form = AppForm(request.POST, request.FILES, instance=app)
        if form.is_valid():
            form.save()
            return redirect('app_list')
    else:
        form = AppForm(instance=app)
    return render(request, 'update_app.html', {'form': form, 'app': app})

@login_required
def delete_app(request, app_id):
    app = get_object_or_404(App, id=app_id, uploaded_by=request.user)
    if request.method == 'POST':
        app.delete()
        return redirect('app_list')
    return render(request, 'delete_app.html', {'app': app})