from django.shortcuts import render, redirect
from django.views.generic import View
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import User
from .deploy import *
from .models import *
from .ipfsFiles import *
from .decorator import *


class loginView(View):
    def get(self, request, *args, **kwargs):
        if request.user.get_username() != "":
            return redirect("main:home")
        form = AuthenticationForm()
        return render(request, "login.html", {"form": form})

    def post(self, request, *args, **kwargs):
        form = AuthenticationForm(request.POST)
        username = request.POST["username"]
        password = request.POST["password"]
        if User.objects.filter(username=username).exists():
            user = User.objects.get(username=username)
            if user.check_password(password):
                user_authenticated = authenticate(
                    request, username=username, password=password
                )
                login(request, user_authenticated)
                typeOfUser = modUser.objects.get(user=user)
                if typeOfUser.typeOfUser:
                    request.session["uploader"] = True
                else:
                    request.session["verifier"] = True
                return redirect("main:home")
            else:
                return render(
                    request,
                    "login.html",
                    {
                        "form": form,
                        "my_messages": {"error": "Invalid Credentials."},
                    },
                )
        else:
            return render(
                request,
                "login.html",
                {"form": form, "my_messages": {"error": "Invalid Credentials."}},
            )


class logoutView(View):
    @redirector("logout")
    def get(self, request, *args, **kwargs):
        logout(request)
        return redirect("main:loginView")


class homepage(View):
    @redirector("home")
    def get(self, request, *args, **kwargs):
        return render(request, "home.html")


class uploadPage(View):
    @redirector("upload")
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


class verifyPage(View):
    @redirector("verify")
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


class updatePage(View):
    @redirector("update")
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
