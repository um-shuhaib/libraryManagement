from django.shortcuts import render,redirect
from django.http import HttpResponse
from django.views import View
from libraryApp.forms import UserRegisterForm,AddBookForm
from django.core.mail import send_mail,settings
from libraryApp.models import User,Category,Book,Issue
from django.contrib.auth import authenticate,login,logout

# Create your views here.
def send_otp(user_instance):
    user_instance.generate_otp()

class RegisterView(View):
    def get(self,request):
        form=UserRegisterForm()
        return render(request,"register.html",{"form":form})
    
    def post(self,request):
        form_instance = UserRegisterForm(request.POST,request.FILES)
        if form_instance.is_valid():
            user_instance = form_instance.save(commit=False) # user creation form is used so the pass will hashed 
            user_instance.is_active = False
            user_instance.save()
            send_otp(user_instance)
            send_mail("Confirm The OTP",user_instance.otp,settings.EMAIL_HOST_USER,[user_instance.email])
            return redirect("otpverify")
            # return HttpResponse("otp verification")
        else:
            return redirect("register")
            # return HttpResponse("not valid")

class VerifyOTPView(View):
    def get(self,request):
        return render(request,"otp_verify.html")
    def post(self,request):
        otp=request.POST.get("otp")
        try:
            user_instance=User.objects.get(otp=otp)
            user_instance.is_active=True
            user_instance.is_verified=True
            user_instance.otp=""
            user_instance.save()
            # return redirect("login")
            return redirect("login")
        except:
            return redirect("otpverify")
class LoginView(View):
    def get(self,request):
        # form=LoginForm()
        return render(request,"login.html")
    def post(self,request):
        username=request.POST.get("username")
        password=request.POST.get("password")
        res = authenticate(request,username=username,password=password)
        if res:
            login(request,res)
            if res.role=="user":
                return HttpResponse("User login Successfull")
            else:
                return redirect("dashboard")

        else:
            return HttpResponse("login Not Successfull")
        
class DashboardView(View):
    def get(self,request):
        books=Book.objects.filter(avl_copy__gt = 0)
        return render(request,"dashboard.html",{"books":books})
    
class MailVerifyView(View):
    def get(self,request):
        return render(request,"password.html")
    
    def post(self,request):
        user=User.objects.get(email=request.POST.get("email"))
        if user.is_active:
            send_otp(user)
            send_mail("Confirm The OTP for Restting the Password",user.otp,settings.EMAIL_HOST_USER,[user.email])
            return redirect("otp-password")
        else:
            return redirect("password")
class OtpPasswordView(View):
    def get(self,request):
        return render(request,"otp-password.html")
    def post(self,request):
        otp=request.POST.get("otp")
        try:
            user_instance=User.objects.get(otp=otp)
            
            user_instance.otp=""
            user_instance.save()
            return redirect("change-password",user=user_instance.id)
        except:
            return redirect("otp-password")
        
class ChangePasswordView(View):
    def get(self,request,**kwargs):
        return render(request,"changepassword.html")
    def post(self,request,**kwargs):
        user=User.objects.get(id=kwargs.get("user"))
        user.set_password(request.POST.get("password"))        
        user.save()
        return redirect("login")

class AddCategoryView(View):
    def get(self,request):
        category=Category.objects.all()
        return render(request,"addcategory.html",{"category":category})
    def post(self,request):
        category=request.POST.get("category")
        Category.objects.create(category=category)
        return redirect("category")
        
    
class AddBookView(View):
    def get(self,request):
        form=AddBookForm()
        return render(request,"addbook.html",{"form":form})
    def post(self,request):
        form_instance=AddBookForm(request.POST,request.FILES)
        total=request.POST.get("total_copy")
        if form_instance.is_valid():
            book=form_instance.save(commit=False)
            book.user=request.user
            book.avl_copy=total
            book.save()
            # Step 2: Save M2M categories
            form_instance.save_m2m()
            return redirect("book")

class IssueBookView(View):
    def get(self, request):
        books=Book.objects.filter(avl_copy__gt = 0)
        issued=Issue.objects.all()
        return render(request,"issuebook.html",{"books":books,"issued":issued})

class IssueUserView(View):
    def get(self,request,**kwargs):
        book=Book.objects.get(id=kwargs.get("id"))
        users=User.objects.filter(role="user")
        return render(request,"issueuser.html",{"book":book,"users":users})