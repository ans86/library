from django.shortcuts import get_object_or_404
from django.http import FileResponse, Http404
import mimetypes
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Book



# @login_required
# def publish_book(request):
#     if request.method == 'POST':
#         title = request.POST.get('title')
#         description = request.POST.get('description')
#         book_file = request.FILES.get('book_file')
#         cover_image = request.FILES.get('cover_image')
        
        

#         if not book_file or not book_file.name.endswith('.pdf'):
#             messages.error(request, "Please upload a valid PDF file.")
#             return redirect('publish_book')

#         book = Book.objects.create(
#             author=request.user,
#             title=title,
#             description=description,
#             file=book_file,
#             cover_image=cover_image
#         )

#         messages.success(request, f"Book '{book.title}' published successfully!")
#         return redirect('publish_book')
    
#     if not request.user.has_perm('books.can_upload_books'):
#         return redirect('home')

#     return render(request, 'books/publish_book.html')



def publish_book(request):
    # ✅ Access check
    if not request.user.is_authenticated:
        messages.error(request, "You must be logged in to publish a book.")
        return redirect('home')

    if not (request.user.is_staff or request.user.role == 'author' or request.user.can_upload_books):
        messages.warning(request, "You don't have permission to publish books.")
        return redirect('home')

    if request.method == 'POST':
        title = request.POST.get('title')
        description = request.POST.get('description')
        file = request.FILES.get('file')
        cover_image = request.FILES.get('cover_image')

        if title and file:
            Book.objects.create(
                author=request.user,
                title=title,
                description=description,
                file=file,
                cover_image=cover_image
            )
            messages.success(request, "Book published successfully!")
            return redirect('home')

    return render(request, 'books/publish_book.html')

# def read_book(request, slug):
#     book = get_object_or_404(Book, slug=slug)

#     # Optional: only allow if approved or staff
#     if not book.is_approved and not request.user.is_staff:
#         raise Http404("This book is not available yet.")

#     file_path = book.file.path
#     file = open(file_path, 'rb')
#     mime_type, _ = mimetypes.guess_type(file_path)
#     response = FileResponse(file, content_type=mime_type)
#     response['Content-Disposition'] = f'inline; filename="{book.title}.pdf"'
#     return response
    
    
    
    
    
def read_book(request, slug):
    book = get_object_or_404(Book, slug=slug)
    return redirect(book.file.url)