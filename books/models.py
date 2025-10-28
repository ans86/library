import os
from django.db import models
from django.conf import settings
from django.utils.text import slugify


class Book(models.Model):
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    slug = models.SlugField(unique=True, blank=True)  # new field
    cover_image = models.ImageField(upload_to='book_covers/', blank=True, null=True)
    file = models.FileField(upload_to='books/')
    description = models.TextField(blank=True)
    published_at = models.DateTimeField(auto_now_add=True)
    is_approved = models.BooleanField(default=False)

    def save(self, *args, **kwargs):
        if not self.slug and self.file:
            # PDF ka base name lete hain (sirf naam, extension ke bina)
            filename = os.path.splitext(os.path.basename(self.file.name))[0]
            # slugify kar ke slug me daal do
            self.slug = slugify(filename)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title

    class Meta:
        permissions = [
            ("can_publish_book", "Can publish books"),
        ]





# class Book(models.Model):
#     author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
#     title = models.CharField(max_length=200)
#     cover_image = models.ImageField(upload_to='book_covers/', blank=True, null=True)
#     file = models.FileField(upload_to='books/')
#     description = models.TextField(blank=True)
#     published_at = models.DateTimeField(auto_now_add=True)
#     is_approved = models.BooleanField(default=False)  # Admin approval (optional)

#     def __str__(self):
#         return self.title
    
#     class Meta:
#         permissions = [
#             ("can_publish_book", "Can publish books"),
#         ]

