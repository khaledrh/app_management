from django.urls import path, include
from . import views
from django.contrib.auth import views as auth_views

app_name = 'users'

urlpatterns = [
    # path('', views.home, name='home'),
    path('register/', views.register_view, name='register'),
    # path('apps/', include('apps.urls')),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
]