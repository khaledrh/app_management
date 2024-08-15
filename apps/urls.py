from django.urls import path
from . import views

urlpatterns = [
    path('', views.app_list, name='app_list'),
    path('add/', views.add_app, name='add_app'),
    path('update/<int:app_id>/', views.update_app, name='update_app'),
    path('delete/<int:app_id>/', views.delete_app, name='delete_app'),
]