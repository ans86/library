from django.urls import path
from . import views

urlpatterns = [
    path('publish/', views.publish_book, name='publish_book'),
    path('read/<slug:slug>/', views.read_book, name='read_book'),
]
