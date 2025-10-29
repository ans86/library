import os
from django.db import models
from django.conf import settings
from django.utils.text import slugify


class Book(models.Model):
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="books"
    )
    title = models.CharField(max_length=200)
    slug = models.SlugField(unique=True, blank=True)
    cover_image = models.ImageField(upload_to='book_covers/', blank=True, null=True)
    description = models.TextField(blank=True)
    published_at = models.DateTimeField(auto_now_add=True)
    is_approved = models.BooleanField(default=False)  # Staff approval

    def save(self, *args, **kwargs):
        # Slug bana lo agar nahi bana hua
        if not self.slug:
            if self.title:
                self.slug = slugify(self.title)
            elif self.file:
                filename = os.path.splitext(os.path.basename(self.file.name))[0]
                self.slug = slugify(filename)

        super().save(*args, **kwargs)

    def __str__(self):
        return self.title

    class Meta:
        permissions = [
            ("can_publish_book", "Can publish books"),
        ]


class Chapter(models.Model):
    book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name='chapters')
    title = models.CharField(max_length=200)
    content = models.TextField()
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['order']

    def __str__(self):
        return f"{self.book.title} - {self.title}"