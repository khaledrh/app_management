from django.shortcuts import render
from .models import App

def app_list(request):
    apps = App.objects.filter(uploaded_by=request.user)
    return render(request, 'apps/app_list.html', {'apps': apps})
