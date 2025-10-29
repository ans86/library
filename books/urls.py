from django.urls import path
from . import views

urlpatterns = [
    path('search', views.search_books, name='search_books'),
    path('publish/', views.publish_book, name='publish_book'),
    path('dashboard/', views.staff_dashboard, name='staff_dashboard'),
    path('dashboard/books', views.book_dashboard, name='book_dashboard'),
    path('dashboard/authors', views.author_dashboard, name='author_dashboard'),
    path('approve-author/<int:author_id>/', views.approve_author, name='approve_author'),
    path('approve-book/<int:book_id>/', views.approve_book, name='approve_book'),
    path('reject-book/<int:book_id>/', views.reject_book, name='reject_book'),
    path('read/<slug:slug>/', views.read_book, name='read_book'),
    path('write/', views.author_dashboard, name='author_dashboard'),
    path('write/<slug:slug>/', views.write_book, name='write_book'),

]
