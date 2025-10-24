from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Book

@login_required
def publish_book(request):
    if not request.user.can_upload_books:
        messages.error(request, "You are not allowed to upload books.")
        return redirect("home")

    if request.method == "POST":
        title = request.POST.get("title")
        description = request.POST.get("description")
        file = request.FILES.get("file")

        if not title or not file:
            messages.error(request, "Title and file are required.")
            return redirect("publish_book")

        book = Book.objects.create(
            title=title,
            author=request.user,
            description=description,
            file=file
        )
        messages.success(request, "Book uploaded successfully! Waiting for admin approval.")
        return redirect("home")

    return render(request, "books/publish_book.html")
    