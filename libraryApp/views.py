from django.shortcuts import render,redirect
from django.http import HttpResponse
from django.views import View
from libraryApp.forms import UserRegisterForm,AddBookForm,UserUpdationForm
from django.core.mail import send_mail,settings
from libraryApp.models import User,Category,Book,Issue
from django.contrib.auth import authenticate,login,logout
from datetime import date, timedelta
from django.contrib import messages
from libraryApp.authentication import login_required
from django.utils.decorators import method_decorator

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
            messages.success(request,"Email OTP send Succefully")
            return redirect("otpverify")
        else:
            messages.warning(request,"Not Registered : Must be unique username and email and confirm the password correctly")
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
            messages.success(request,"OTP Verification Succeful")
            return redirect("login")
        except:
            messages.warning(request,"Invalid OTP - Try Again")
            return redirect("otpverify")
        
class LoginView(View):
    def get(self,request):
        return render(request,"login.html")
    def post(self,request):
        username=request.POST.get("username")
        password=request.POST.get("password")
        res = authenticate(request,username=username,password=password)
        if res:
            login(request,res)
            messages.success(request,"Login Succeful")
            if res.role=="user":
                return redirect("home")
            else:
                return redirect("dashboard")

        else:
            messages.warning(request,"Invalid Credentials")
            return redirect("login")

@method_decorator(login_required,name="dispatch")     
class DashboardView(View):
    def get(self,request):
        books=Book.objects.all()
        return render(request,"dashboard.html",{"books":books})
    
class MailVerifyView(View):
    def get(self,request):
        return render(request,"password.html")
    
    def post(self,request):
        try:
            user=User.objects.get(email=request.POST.get("email"))
        except:
            messages.error(request,"Invalid Credential")
            return redirect("password")

        if user.is_active:
            send_otp(user)
            send_mail("Confirm The OTP for Restting the Password",user.otp,settings.EMAIL_HOST_USER,[user.email])
            messages.success(request,"Email-OTP Send Succefully")
            return redirect("otp-password")
        else:
            messages.error(request,"Invalid Credential")
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
            messages.success(request,"OTP Verification Succeful")
            return redirect("change-password",user=user_instance.id)
        except:
            messages.warning(request,"OTP is Invalid")
            return redirect("otp-password")
        
class ChangePasswordView(View):
    def get(self,request,**kwargs):
        return render(request,"changepassword.html")
    def post(self,request,**kwargs):
        user=User.objects.get(id=kwargs.get("user"))
        user.set_password(request.POST.get("password"))        
        user.save()
        messages.success(request,"Password Changed Succefully")
        return redirect("login")

@method_decorator(login_required,name="dispatch")
class AddCategoryView(View):
    def get(self,request):
        category=Category.objects.all()
        return render(request,"addcategory.html",{"category":category})
    def post(self,request):
        category=request.POST.get("category")
        Category.objects.create(category=category)
        messages.success(request,"New Category Added")
        return redirect("category")
        
@method_decorator(login_required,name="dispatch")
class AddBookView(View):
    def get(self,request):
        form=AddBookForm()
        books=Book.objects.all()
        return render(request,"addbook.html",{"form":form,"books":books})
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
            messages.success(request,"New Book Added")
            return redirect("book")
        else:
            messages.error(request,"Book Not Added")
            return redirect("book")
        
@method_decorator(login_required,name="dispatch")
class IssueBookView(View):
    def get(self, request):
        books=Book.objects.filter(avl_copy__gt = 0)
        issued=Issue.objects.all()
        return render(request,"issuebook.html",{"books":books,"issued":issued})

@method_decorator(login_required,name="dispatch")
class IssueUserView(View):
    def get(self,request,**kwargs):
        book=Book.objects.get(id=kwargs.get("id"))
        users=User.objects.filter(role="user")
        return render(request,"issueuser.html",{"book":book,"users":users})
        

class IssuedView(View):
    def get(self,request,**kwargs):
        book=Book.objects.get(id=kwargs.get("book_id"))
        user=User.objects.get(id=kwargs.get("user_id"))
        Issue.objects.create(user=user,book=book,due_date=date.today() + timedelta(days=7))
        book.avl_copy -= 1
        book.save()
        messages.success(request,"Book Issued")
        return redirect("issue")
    
@method_decorator(login_required,name="dispatch")
class UpdateBookView(View):
    def get(self,request,**kwargs):
        book=Book.objects.get(id=kwargs.get("id"))
        form=AddBookForm(instance=book)
        return render(request,"updatebook.html",{"form":form})
    def post(self,request,**kwargs):
        book=Book.objects.get(id=kwargs.get("id"))
        form_instance=AddBookForm(request.POST,request.FILES,instance=book)
        if form_instance.is_valid():
            book=form_instance.save(commit=False)
            book.user=request.user
            book.save()
            form_instance.save_m2m()
            messages.success(request,"Book Updated")
            return redirect("book")
        else:
            messages.error(request,"Not updated")
            return redirect("update")

@method_decorator(login_required,name="dispatch")     
class DeleteBookView(View):
    def get(self,request,**kwargs):
        book=Book.objects.get(id=kwargs.get("id"))
        book.delete()
        messages.success(request,"Book Deleted")
        return redirect("book")

@method_decorator(login_required,name="dispatch")  
class EditCategoryView(View):
    def get(self,request,**kwargs):
        category=Category.objects.get(id=kwargs.get("id"))
        return render(request,"editcategory.html",{"category":category})
    def post(self,request,**kwargs):
        category=Category.objects.get(id=kwargs.get("id"))
        cat=request.POST.get("category")
        category.category=cat
        category.save()
        messages.success(request,"Category Edited")
        return redirect("category")

@method_decorator(login_required,name="dispatch")
class DeleteCategoryView(View):
    def get(self,request,**kwargs):
        cat=Category.objects.get(id=kwargs.get("id"))
        cat.delete()
        messages.success(request,"Category Deleted")
        return redirect("category")

@method_decorator(login_required,name="dispatch")
class returnBookView(View):
    def get(self,request,**kwargs):
        issue=Issue.objects.get(id=kwargs.get("id"))
        if date.today() > issue.due_date and issue.status != "returned":
            days = (date.today() - issue.due_date).days
            issue.fine = days * 5
            issue.status = "overdue"
            issue.save()
        history=Issue.objects.filter(user=issue.user)
        return render(request,"return.html",{"issue":issue,"history":history})

class ReturnAcceptView(View):
    def get(self,request,**kwargs):
        issue=Issue.objects.get(id=kwargs.get("id"))
        if issue.status == "issued":
            issue.status="returned"
            issue.returned_date=date.today()
            issue.fine = 0
            book = issue.book
            book.avl_copy += 1
            book.save()
            issue.save()
            messages.success(request,"Book Returned")
            return redirect("issue")
        else:
            messages.warning(request, "This book is already returned.")
            return redirect("issue")

@method_decorator(login_required,name="dispatch")
class UserDetailsView(View):
    def get(self,request):
        users=User.objects.filter(role="user")
        return render(request,"userdetail.html",{"users":users})

@method_decorator(login_required,name="dispatch")    
class UserUpdateView(View):
    def get(self,request,**kwargs):
        user=User.objects.get(id=kwargs.get("id"))
        form=UserUpdationForm(instance=user)
        return render(request,"updateuser.html",{"form":form})
    def post(self,request,**kwargs):
        user=User.objects.get(id=kwargs.get("id"))
        form_instance=UserUpdationForm(request.POST,request.FILES,instance=user)
        if form_instance.is_valid():
            form_instance.save()
            messages.success(request,"User Updated")
            return redirect("user")
        else:
            messages.error(request,"User Not Updated")
            return redirect("userupdate")

@method_decorator(login_required,name="dispatch")    
class DeleteUserView(View):
    def get(self,request,**kwargs):
        user=User.objects.get(id=kwargs.get("id"))
        user.delete()
        messages.success(request,"User Removed")
        return redirect("user")
    
class LogoutView(View):
    def get(self,request):
        logout(request)
        messages.success(request,"User Logout")
        return redirect("login")
    
class ProfileView(View):
    def get(self,request):
        user=request.user
        history=Issue.objects.filter(user=user)
        return render(request,"profile.html",{"user":user,"history":history})
    
class ProfileUpdateView(View):
    def get(self,request,**kwargs):
        user=User.objects.get(id=kwargs.get("id"))
        form=UserUpdationForm(instance=user)
        return render(request,"updateuser.html",{"form":form})
    def post(self,request,**kwargs):
        user=User.objects.get(id=kwargs.get("id"))
        form_instance=UserUpdationForm(request.POST,request.FILES,instance=user)
        if form_instance.is_valid():
            form_instance.save()
            messages.success(request,"Profile Updated")
            return redirect("profile")
        else:
            messages.error(request,"Profile Not Updated")
            return redirect("profileupdate")