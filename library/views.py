from django.http import HttpResponse
from django.shortcuts import render
from books.models import Book


def home(request):
    books = Book.objects.all()
    return render(request, 'home.html', {'books': books})



# def home(request):
#     books = Book.objects.filter(is_approved=True).order_by('-published_at')  # latest first
#     return render(request, 'home.html', {'books': books})