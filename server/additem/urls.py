# additem/urls.py
from django.urls import path
from .views import items_view

urlpatterns = [
    # /api/items/ -> GET, POST
    path('items/', items_view, name='items_view'),
]
