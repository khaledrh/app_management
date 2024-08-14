from django.urls import path
from . import views

urlpatterns = [
    path('app_list/', views.app_list, name='app_list'),
]