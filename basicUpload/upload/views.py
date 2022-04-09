from django.shortcuts import render
from django.views.generic import View
from .models import modUser
from django.contrib.auth import authenticate, login, logout
from django.urls import reverse
from django.http import HttpResponseRedirect
from django.db import IntegrityError
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.utils.safestring import mark_safe
from .ipfsFiles import download_image
# Create your views here.


class homepage(View):
    def get(self, request, *args, **kwargs):
        return render(request, "upload/home.html")


class loginView(View):
    def get(self, request, *args, **kwargs):
        if "uploader" in request.session:
            return HttpResponseRedirect(reverse("uploadPage"))
        if "verifier" in request.session:
            return HttpResponseRedirect(reverse("verifyPage"))
        return render(request, "upload/login.html")

    def post(self, request, *args, **kwargs):
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = authenticate(request, username=username, password=password)
        if user is not None:
            typeOfUser = modUser.objects.get(user=user)
            login(request, user)
            if typeOfUser.typeOfUser:
                request.session["uploader"] = True
                return HttpResponseRedirect(reverse("uploadPage"))
            else:
                request.session["verifier"] = True
                return HttpResponseRedirect(reverse("verifyPage"))


class uploadPage(LoginRequiredMixin, View):
    login_url = "/login"

    def get(self, request, *args, **kwargs):
        if "uploader" not in request.session:
            return HttpResponseRedirect(reverse("home"))
        return render(request, "upload/uploadPage.html")
    def post(self, request, *args, **kwargs):
        # type = request.POST.get("type")
        # passNum = request.POST.get("passNum")
        # holderName = request.POST.get("holderName")
        # gender = request.POST.get("gender")
        dob = request.POST.get("dob")
        # placeOfBirth = request.POST.get("placeOfBirth")
        # placeOfIssue = request.POST.get("placeOfIssue")
        # dateOfIssue = request.POST.get("dateOfIssue")
        # dateOfExpiry = request.POST.get("dateOfExpiry")
        faceId = request.FILES.get("faceId")
        # sign = request.FILES.get("sign")
        # father = request.POST.get("father")
        # mother = request.POST.get("mother")
        # spouse = request.POST.get("spouse")
        # address_1 = request.POST.get("address_1")
        # address_2 = request.POST.get("address_2")
        # address_3 = request.POST.get("address_3")
        # address_4 = request.POST.get("address_4")
        # oldPassNum = request.POST.get("oldPassNum")
        # oldPlaceIssue = request.POST.get("oldPlaceIssue")
        # oldDateIssue = request.POST.get("oldDateIssue")
        # fileNum = request.POST.get("fileNum")
        print(dob)
        print(type(faceId.read()))
        return HttpResponseRedirect(reverse("uploadPage"))
        
class verifyPage(LoginRequiredMixin, View):
    login_url = "/login"

    def get(self, request, *args, **kwargs):
        if "verifier" not in request.session:            
            return HttpResponseRedirect(reverse("home"))
        # image = download_image()
        return render(request, "upload/verifyPage.html", context = {
            "img": "",
            })


class logoutView(View):
    def get(self, request, *args, **kwargs):
        try:
            logout(request)
        except:
            pass
        return HttpResponseRedirect(reverse("home"))
