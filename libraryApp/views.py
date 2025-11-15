from django.shortcuts import render,redirect
from django.http import HttpResponse
from django.views import View
from libraryApp.forms import UserRegisterForm
from django.core.mail import send_mail,settings
from libraryApp.models import User
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
        return render(request,"dashboard.html")
    
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


    
