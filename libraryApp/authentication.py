
from django.shortcuts import redirect
from django.contrib import messages

def login_required(fn):
    def wrapper(request, *args, **kwargs):
        if request.user.is_authenticated and request.user.role != "user" :
            return fn(request, *args, **kwargs) 
        else:
            messages.warning(request,"You Must Login First")
            return redirect("login")
    return wrapper