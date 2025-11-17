from django.db import models
from django.contrib.auth.models import AbstractUser
from random import randint
from datetime import date


# Create your models here.
class User(AbstractUser):
    email=models.EmailField(unique=True)
    option = (
        ('user','user'),
        ('staff','staff')
    )
    phone=models.CharField(max_length=15)
    role=models.CharField(max_length=100,choices=option,default="user")
    profile=models.ImageField(upload_to="profile",default="profile/default.jpeg",null=True,blank=True)
    otp=models.CharField(max_length=20)
    is_verified=models.BooleanField(default=False)

    #random otp generation
    def generate_otp(self):
        send_otp=str(randint(1000,9999))+str(self.id) # for making unique is , added userid at the end
        self.otp=send_otp
        self.save()

class Category(models.Model):
    category=models.CharField(max_length=20,unique=True)

    def __str__(self):
        return self.category


class Book(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE,related_name="bookUser")
    title=models.CharField(max_length=100)
    author=models.CharField(max_length=20)
    isbn=models.IntegerField()
    image=models.ImageField(upload_to="books",default="books/default.jpeg",null=True,blank=True)
    category=models.ManyToManyField(Category,related_name="bookCategory")
    total_copy=models.IntegerField()
    avl_copy=models.IntegerField()
    added_on=models.DateField(auto_now_add=True)

    def __str__(self):
        return self.title

class Issue(models.Model):
    STATUS = (
        ('issued', 'Issued'),
        ('returned', 'Returned'),
        ('overdue', 'Overdue'),
    )

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="issued_by")
    book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name="issued_book")
    issue_date = models.DateField(auto_now_add=True)
    due_date = models.DateField()
    returned_date = models.DateField(null=True, blank=True)
    fine = models.IntegerField(default=0)
    status = models.CharField(max_length=10, choices=STATUS, default="issued")

    def __str__(self):
        return f"{self.book.title} → {self.user.username}"

