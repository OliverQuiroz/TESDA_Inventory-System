from django.urls import path
from .views import items_view, item_detail_view

urlpatterns = [
    # GET all items or POST a new item
    path('items/', items_view, name='items_view'),

    # GET/PUT/DELETE a single item by primary key
    path('items/<int:pk>/', item_detail_view, name='item_detail_view'),
]
