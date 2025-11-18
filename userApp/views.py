from django.shortcuts import render
from django.views import View
from libraryApp.models import Book,Issue

# Create your views here.
class UserHomeView(View):
    def get(self,request):
        books=Book.objects.filter(avl_copy__gt = 0 )
        return render(request,"home.html",{"books":books})
    
class ProfileView(View):
    def get(self,request):
        user=request.user
        history=Issue.objects.filter(user=user)
        return render(request,"userprofile.html",{"user":user,"history":history})