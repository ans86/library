from django.db.models import Q
from django.shortcuts import get_object_or_404
from django.http import FileResponse, Http404
import mimetypes
from users.models import CustomUser
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Book, Chapter


def search_books(request):
    query = request.GET.get('q', '')
    books = Book.objects.filter(Q(title__icontains=query) | Q(description__icontains=query))
    return render(request, 'search_results.html', {'books': books, 'query': query})




@login_required
def publish_book(request):
    # Role-based access control
    user = request.user
    if not (user.is_staff or (user.role == 'author' and user.can_upload_books)):
        messages.warning(request, "You don't have permission to publish books.")
        return redirect('home')

    if request.method == 'POST':
        title = request.POST.get('title')
        description = request.POST.get('description')
        cover_image = request.FILES.get('cover_image')

        # Validation
        if not title or not cover_image:
            messages.error(request, "Title and cover image are required.")
            return redirect('publish_book')
        
        #Check for unique title
        if Book.objects.filter(title__iexact=title).exists():
            messages.error(request, "A book with this title already exists.")
            return redirect('publish')


        # Book is created but not approved (staff will approve later)
        book = Book.objects.create(
            author=user,
            title=title,
            description=description,
            cover_image=cover_image,
            is_approved=False  # Always False by default
        )

        messages.success(
            request,
            "Book submitted successfully! Please wait for staff approval."
        )
        return redirect('home')

    return render(request, 'books/publish_book.html')

@login_required
def staff_dashboard(request):
    # Only staff can access
    if not request.user.is_staff:
        messages.warning(request, "You are not authorized to access the staff dashboard.")
        return redirect('home')

    # All authors (for full view)
    all_authors = CustomUser.objects.filter(role='author')

    # All books
    all_books = Book.objects.all()

    context = {
        'all_authors': all_authors,
        'all_books': all_books,
    }
    return render(request, 'books/staff_dashboard.html', context)



@login_required
def book_dashboard(request):
    # Only staff can access
    if not request.user.is_staff:
        messages.warning(request, "You are not authorized to access the book dashboard.")
        return redirect('home')
    # Get all unapproved books
    pending_books = Book.objects.filter(is_approved=False)

    context = {
        'pending_books': pending_books,
    }
    return render(request, 'books/book_dashboard.html', context)



@login_required
def approve_author(request, author_id):
    if not request.user.is_staff:
        messages.warning(request, "Access denied!")
        return redirect('home')

    author = get_object_or_404(CustomUser, id=author_id, role='author')
    author.can_upload_books = True
    author.save()
    messages.success(request, f"Author '{author.username}' is now approved to upload books.")
    return redirect('staff_dashboard')


@login_required
def approve_book(request, book_id):
    if not request.user.is_staff:
        messages.warning(request, "Access denied!")
        return redirect('home')

    book = get_object_or_404(Book, id=book_id)
    book.is_approved = True
    book.save()
    messages.success(request, f"Book '{book.title}' approved successfully!")
    return redirect('staff_dashboard')


@login_required
def reject_book(request, book_id):
    if not request.user.is_staff:
        messages.warning(request, "Access denied!")
        return redirect('home')

    book = get_object_or_404(Book, id=book_id)
    book.delete()
    messages.info(request, f"Book '{book.title}' rejected and removed.")
    return redirect('staff_dashboard')


def read_book(request, slug):
    book = get_object_or_404(Book, slug=slug, is_approved=True)
    chapters = book.chapters.all()  # Related_name se mila
    return render(request, 'books/read_book.html', {'book': book, 'chapters': chapters})




@login_required
def author_dashboard(request):
    # Show only books of the logged-in author that are approved
    books = Book.objects.filter(author=request.user, is_approved=True)
    return render(request, 'books/write.html', {'books': books})


@login_required
def write_book(request, slug):
    book = get_object_or_404(Book, slug=slug)

    # check if this user is the author of this book
    if book.author != request.user:
        messages.warning(request, "You are not allowed to write this book.")
        return redirect('write')

    # agar POST request (chapter likha ja raha hai)
    if request.method == "POST":
        title = request.POST.get("title")
        content = request.POST.get("content")

        # chapter add karte hain
        Chapter.objects.create(book=book, title=title, content=content)
        messages.success(request, "Chapter added successfully!")
        return redirect('write_book', slug=book.slug)

    chapters = book.chapters.all()
    return render(request, 'books/write_book.html', {'book': book, 'chapters': chapters})
    

    
