from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('login.urls')),
    path('api/', include('additem.urls')),
]
