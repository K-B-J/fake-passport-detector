from django.shortcuts import render
from django.views.generic import View
from .models import modUser
from django.contrib.auth import authenticate, login, logout
from django.urls import reverse
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from .deploy import *
from .ipfsFiles import *


class homepage(View):
    def get(self, request, *args, **kwargs):
        return render(request, "home.html")


class loginView(View):
    def get(self, request, *args, **kwargs):
        if "uploader" in request.session:
            return HttpResponseRedirect(reverse("uploadPage"))
        if "verifier" in request.session:
            return HttpResponseRedirect(reverse("verifyPage"))
        return render(request, "login.html")

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
        return render(request, "uploadPage.html")

    def post(self, request, *args, **kwargs):
        typeOfPass = request.POST.get("type")
        passNum = request.POST.get("passNum")
        holderName = request.POST.get("holderName")
        countryCode = request.POST.get("countryCode")
        nationality = request.POST.get("nationality")
        surname = request.POST.get("surname")
        gender = request.POST.get("gender")
        dob = request.POST.get("dob")
        placeOfBirth = request.POST.get("placeOfBirth")
        placeOfIssue = request.POST.get("placeOfIssue")
        dateOfIssue = request.POST.get("dateOfIssue")
        dateOfExpiry = request.POST.get("dateOfExpiry")
        faceId = request.FILES.get("faceId")
        sign = request.FILES.get("sign")
        father = request.POST.get("father")
        mother = request.POST.get("mother")
        spouse = request.POST.get("spouse")
        address_1 = request.POST.get("address_1")
        address_2 = request.POST.get("address_2")
        address_3 = request.POST.get("address_3")
        address_4 = request.POST.get("address_4")
        oldPassNum = request.POST.get("oldPassNum")
        oldPlaceIssue = request.POST.get("oldPlaceIssue")
        oldDateIssue = request.POST.get("oldDateIssue")
        oldPassNumDateAndIssue = (
            oldPassNum + " " + str(oldDateIssue) + " " + str(oldPlaceIssue)
        )
        fileNum = request.POST.get("fileNum")
        faceIdHash = upload_image(faceId.name, faceId.read())
        signIdHash = upload_image(sign.name, sign.read())
        address = address_1 + ";" + address_2 + ";" + address_3 + ";" + address_4
        personal_info = [
            surname,
            holderName,
            nationality,
            gender,
            str(dob),
            placeOfBirth,
            father,
            mother,
            spouse,
            address,
        ]
        imagesInfo = [faceIdHash, signIdHash]
        passportInfo = [
            typeOfPass,
            countryCode,
            placeOfIssue,
            str(dateOfIssue),
            str(dateOfExpiry),
            oldPassNumDateAndIssue,
            fileNum,
        ]
        print(
            new_passport(
                passnum=passNum,
                personal_info=personal_info,
                imagesInfo=imagesInfo,
                passportInfo=passportInfo,
            )
        )
        return HttpResponseRedirect(reverse("uploadPage"))


class verifyPage(LoginRequiredMixin, View):
    login_url = "/login"

    def get(self, request, *args, **kwargs):
        return render(request, "verifyPage.html", context={"get_details": False})

    def post(self, request, *args, **kwargs):
        passNum = request.POST.get("passNum")
        all_details = get_passport_details(passNum)
        if "uploader" in request.session:
            update_access = True
        else:
            update_access = False
        if not all_details["success"]:
            context = {
                "get_details": False,
                "update_access": False,
                "error": all_details["data"],
            }
        else:
            details = all_details["data"]
            passport_num = details[0]
            personalDetailsArr = [
                "surname",
                "name",
                "nationality",
                "sex",
                "dob",
                "placeOfBirth",
                "father",
                "mother",
                "spouse",
                "currentAddress",
            ]
            passportInformationArr = [
                "ptype",
                "countryCode",
                "placeOfIssue",
                "dateOfIssue",
                "dateOfExpiry",
                "oldPassNumDateAndIssue",
                "fileNum",
            ]
            personal_info = {}
            passportInfo = {}

            for index, value in enumerate(details[1:11]):
                personal_info[personalDetailsArr[index]] = value
            for index, value in enumerate(details[13:]):
                passportInfo[passportInformationArr[index]] = value
            personal_info["currentAddress"] = personal_info["currentAddress"].split(";")
            passportInfo["oldPassNumDateAndIssue"] = passportInfo[
                "oldPassNumDateAndIssue"
            ].split(";")
            images = [download_image(details[11]), download_image(details[12])]
            context = {
                "get_details": True,
                "images": images,
                "passportInfo": passportInfo,
                "personal_info": personal_info,
                "passport_num": passport_num,
                "update_access": update_access,
            }
        return render(request, "verifyPage.html", context=context)


class logoutView(View):
    def get(self, request, *args, **kwargs):
        try:
            logout(request)
        except:
            pass
        return HttpResponseRedirect(reverse("home"))


class updatePage(LoginRequiredMixin, View):
    login_url = "/login"

    def get(self, request, *args, **kwargs):
        if "uploader" not in request.session:
            return HttpResponseRedirect(reverse("home"))
        all_details = get_passport_details(self.kwargs["passNum"])
        if not all_details["success"]:
            context = {"get_details": False, "error": all_details["data"]}
        else:
            details = all_details["data"]
            passport_num = details[0]
            personalDetailsArr = [
                "surname",
                "name",
                "nationality",
                "sex",
                "dob",
                "placeOfBirth",
                "father",
                "mother",
                "spouse",
                "currentAddress",
            ]
            passportInformationArr = [
                "ptype",
                "countryCode",
                "placeOfIssue",
                "dateOfIssue",
                "dateOfExpiry",
                "oldPassNumDateAndIssue",
                "fileNum",
            ]
            personal_info = {}
            passportInfo = {}

            for index, value in enumerate(details[1:11]):
                personal_info[personalDetailsArr[index]] = value
            for index, value in enumerate(details[13:]):
                passportInfo[passportInformationArr[index]] = value
            personal_info["currentAddress"] = personal_info["currentAddress"].split(";")
            request.session["images"] = [details[11], details[12]]
            images = [download_image(details[11]), download_image(details[12])]
            context = {
                "get_details": True,
                "images": images,
                "passportInfo": passportInfo,
                "personal_info": personal_info,
                "passport_num": passport_num,
            }
        return render(request, "updatePage.html", context=context)

    def post(self, request, *args, **kwargs):
        typeOfPass = request.POST.get("type")
        holderName = request.POST.get("holderName")
        countryCode = request.POST.get("countryCode")
        nationality = request.POST.get("nationality")
        surname = request.POST.get("surname")
        gender = request.POST.get("gender")
        dob = request.POST.get("dob")
        placeOfBirth = request.POST.get("placeOfBirth")
        placeOfIssue = request.POST.get("placeOfIssue")
        dateOfIssue = request.POST.get("dateOfIssue")
        dateOfExpiry = request.POST.get("dateOfExpiry")
        faceId = request.FILES.get("faceId")
        sign = request.FILES.get("sign")
        father = request.POST.get("father")
        mother = request.POST.get("mother")
        spouse = request.POST.get("spouse")
        address_1 = request.POST.get("address_1")
        address_2 = request.POST.get("address_2")
        address_3 = request.POST.get("address_3")
        address_4 = request.POST.get("address_4")
        oldPassNum = request.POST.get("oldPassNum")
        oldPlaceIssue = request.POST.get("oldPlaceIssue")
        oldDateIssue = request.POST.get("oldDateIssue")
        oldPassNumDateAndIssue = (
            oldPassNum + ";" + str(oldDateIssue) + ";" + str(oldPlaceIssue)
        )
        fileNum = request.POST.get("fileNum")
        imagesInfo = request.session["images"]
        if not (faceId is None):
            faceIdHash = upload_image(faceId.name, faceId.read())
            imagesInfo[0] = faceIdHash
        if not (sign is None):
            signIdHash = upload_image(sign.name, sign.read())
            imagesInfo[1] = signIdHash
        address = address_1 + ";" + address_2 + ";" + address_3 + ";" + address_4
        personal_info = [
            surname,
            holderName,
            nationality,
            gender,
            str(dob),
            placeOfBirth,
            father,
            mother,
            spouse,
            address,
        ]

        # imagesInfo = [faceIdHash, signIdHash]
        passportInfo = [
            typeOfPass,
            countryCode,
            placeOfIssue,
            str(dateOfIssue),
            str(dateOfExpiry),
            oldPassNumDateAndIssue,
            fileNum,
        ]
        print(
            update_passport_details(
                passnum=self.kwargs["passNum"],
                personalInfo=personal_info,
                imagesInfo=imagesInfo,
                passportInfo=passportInfo,
            )
        )
        return HttpResponseRedirect(reverse("verifyPage"))
