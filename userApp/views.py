from django.shortcuts import render,redirect
from django.views import View
from libraryApp.models import Book,Issue,User
from datetime import date, timedelta
from libraryApp.forms import UserUpdationForm
from django.contrib import messages
# from userApp.authentication import login_required
# from django.utils.decorators import method_decorator

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

class UserUpdateView(View):
    def get(self,request,**kwargs):
        user=User.objects.get(id=kwargs.get("id"))
        form=UserUpdationForm(instance=user)
        return render(request,"edituserprofile.html",{"form":form})
    def post(self,request,**kwargs):
        user=User.objects.get(id=kwargs.get("id"))
        form_instance=UserUpdationForm(request.POST,request.FILES,instance=user)
        if form_instance.is_valid():
            form_instance.save()
            return redirect("userprofile")
        else:
            messages.error(request,"User Not Updated")
            return redirect("userprofileupdate")