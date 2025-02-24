# login/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.login_view, name='login_view'),
    path('check-auth/', views.check_auth_view, name='check_auth_view'),
    path('logout/', views.logout_view, name='logout_view'),
]
