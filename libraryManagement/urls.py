"""
URL configuration for libraryManagement project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from libraryApp import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path("register/",views.RegisterView.as_view(),name="register"),
    path("register/verify/",views.VerifyOTPView.as_view(),name="otpverify"),
    path("login/",views.LoginView.as_view(),name="login"),
    path("dashboard/",views.DashboardView.as_view(),name="dashboard"),
    path("pass-recovery/",views.MailVerifyView.as_view(),name="password"),
    path("pass-recovery/otp",views.OtpPasswordView.as_view(),name="otp-password"),
    path("pass-recovery/change/<int:user>",views.ChangePasswordView.as_view(),name="change-password"),
    path("addcategory/",views.AddCategoryView.as_view(),name="category"),
    path("addbook/",views.AddBookView.as_view(),name="book"),
    path("issue/",views.IssueBookView.as_view(),name="issue"),
    path("issue/user/<int:id>",views.IssueUserView.as_view(),name="issueuser"),
    path("issue/issued/<int:user_id>/<int:book_id>",views.IssuedView.as_view(),name="issued"),
    path("updatebook/<int:id>",views.UpdateBookView.as_view(),name="update"),
    path("deletebook/<int:id>",views.DeleteBookView.as_view(),name="delete"),
    path("editcategory/<int:id>",views.EditCategoryView.as_view(),name="edit"),
    path("deletecategory/<int:id>",views.DeleteCategoryView.as_view(),name="deletecategory"),

]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
