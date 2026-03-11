from django.contrib import admin
from django.urls import path, include
from shortener import views

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("shortener.urls")),
]