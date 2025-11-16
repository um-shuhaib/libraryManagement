from django.db import models
from libraryApp.models import Book

def library_status(request):
    total_books = Book.objects.count()
    total_copies = Book.objects.aggregate(total=models.Sum("total_copy"))["total"] or 0
    avl_books = Book.objects.aggregate(total=models.Sum("avl_copy"))["total"] or 0


    return {
        "total_books": total_books,
        "total_copies": total_copies,
        "avl_books": avl_books,
    }
