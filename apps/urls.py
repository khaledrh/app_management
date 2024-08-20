from django.urls import path
from . import views

app_name = 'apps'

urlpatterns = [
    path('', views.apps_list, name='list'),
    path('new-app', views.app_new, name='new-app'),
    path('run-test/<int:app_id>/', views.run_appium_test_view, name='run_appium_test'),
    path('<slug:slug>', views.app_page, name='page'),
    path('<slug:slug>/edit/', views.app_update, name='update'),
    path('<slug:slug>/delete/', views.app_delete, name='delete'),
]