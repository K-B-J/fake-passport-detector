from django.shortcuts import render
from django.views.generic import View
from .models import modUser
from django.contrib.auth import authenticate, login, logout
from django.urls import reverse
from django.http import HttpResponseRedirect
from django.db import IntegrityError
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
# Create your views here.

class homepage(View):
    def get(self,request, *args, **kwargs):
        return render(request, "upload/home.html")

class loginView(View):
    def get(self, request, *args, **kwargs):
        return render(request, "upload/login.html")
    def post(self, request, *args, **kwargs):
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = authenticate(request, username=username, password=password)
        print(user.get_username())
        if user is not None:
            typeOfUser = modUser.objects.get(user = user)
            login(request, user)
            if typeOfUser.typeOfUser:
                request.session["uploader"] = True
                return HttpResponseRedirect(reverse("uploadPage"))
            else:
                request.session["verifier"] = True
                return HttpResponseRedirect(reverse("verifyPage"))

class uploadPage(LoginRequiredMixin, View):
    login_url = '/login'
    def get(self, request, *args, **kwargs):
        if "uploader" not in request.session:
            return HttpResponseRedirect(reverse("home"))
        
        return render(request, "upload/uploadPage.html")

class verifyPage(LoginRequiredMixin, View):
    login_url = '/login'
    def get(self, request, *args, **kwargs):
        if "verifier" not in request.session:
            return HttpResponseRedirect(reverse("home"))
        return render(request, "upload/verifyPage.html")

class logoutView(View):
    def get(self, request, *args, **kwargs):
        try:    
            logout(request)
        except:
            pass
        return HttpResponseRedirect(reverse('home'))