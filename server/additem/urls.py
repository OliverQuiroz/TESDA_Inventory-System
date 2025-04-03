from django.urls import path, include
from .views import items_view, item_detail_view
from rest_framework.routers import DefaultRouter
from .views import ItemViewSet

router = DefaultRouter()
router.register(r'items', ItemViewSet)

urlpatterns = [
    path('api/', include(router.urls)),

    # GET all items or POST a new item
    path('items/', items_view, name='items_view'),

    # GET/PUT/DELETE a single item by primary key
    path('items/<int:pk>/', item_detail_view, name='item_detail_view'),
]
