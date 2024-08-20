from django.urls import path
from . import views

app_name = 'apps'

urlpatterns = [
    path('', views.apps_list, name='list'),
    path('new-app', views.app_new, name='new-app'),
    path('run-test/<int:app_id>/', views.run_appium_test_view, name='run_appium_test'),
    path('<slug:slug>', views.app_page, name='page')
    # path('add/', views.add_app, name='add_app'),
    # path('update/<int:app_id>/', views.update_app, name='update_app'),
    # path('delete/<int:app_id>/', views.delete_app, name='delete_app'),
]