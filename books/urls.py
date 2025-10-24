from django.urls import path
from . import views

urlpatterns = [
    path('publish/', views.publish_book, name='publish_book'),
]
