from django.contrib import admin
from django.urls import path,include
from french import views

urlpatterns = [
    path('', include('french.urls')),
    path('admin/', admin.site.urls),
]
