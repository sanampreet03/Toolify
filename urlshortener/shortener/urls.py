from django.contrib import admin
from django.urls import path
from shortener import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home, name='home'),

    path('file-compress/', views.file_compress, name='file_compress'),
    
    path('image-compress/', views.image_compress, name='image_compress'),

    path('<str:code>/', views.redirect_url, name='redirect_url'),
]