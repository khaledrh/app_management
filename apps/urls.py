from django.urls import path
from . import views

app_name = 'apps'

urlpatterns = [
    path('', views.apps_list, name='list'),
    path('<slug:slug>', views.app_page, name='page')
    # path('add/', views.add_app, name='add_app'),
    # path('update/<int:app_id>/', views.update_app, name='update_app'),
    # path('delete/<int:app_id>/', views.delete_app, name='delete_app'),
]