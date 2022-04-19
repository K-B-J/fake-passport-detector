from django.shortcuts import render, redirect
from django.views.generic import View
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import User
from .deploy import *
from .models import *
from .ipfsFiles import *
from .decorator import *
from .forms import *


class loginView(View):
    def get(self, request, *args, **kwargs):
        if request.user.get_username() != "":
            return redirect("main:home")
        form = AuthenticationForm()
        if "my_messages" in request.session:
            my_messages = request.session["my_messages"]
            del request.session["my_messages"]
            return render(
                request, "login.html", {"form": form, "my_messages": my_messages}
            )
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
                        "my_messages": {
                            "error": True,
                            "message": "Invalid Credentials",
                        },
                    },
                )
        else:
            return render(
                request,
                "login.html",
                {
                    "form": form,
                    "my_messages": {"error": True, "message": "Invalid Credentials"},
                },
            )


class logoutView(View):
    @redirector("logout")
    def get(self, request, *args, **kwargs):
        logout(request)
        request.session["my_messages"] = {
            "success": True,
            "message": "Logged Out Successfully",
        }
        return redirect("main:loginView")


class homepage(View):
    @redirector("home")
    def get(self, request, *args, **kwargs):
        if "my_messages" in request.session:
            my_messages = request.session["my_messages"]
            del request.session["my_messages"]
            return render(request, "home.html", {"my_messages": my_messages})
        return render(request, "home.html")


class uploadPage(View):
    @redirector("upload")
    def get(self, request, *args, **kwargs):
        form = passportDataForm()
        return render(request, "uploadPage.html", {"form": form})

    def post(self, request, *args, **kwargs):
        form = passportDataForm(request.POST, request.FILES)
        if form.is_valid():
            typeOfPass = form.cleaned_data["type"]
            passNum = form.cleaned_data["passNum"]
            holderName = form.cleaned_data["holderName"]
            countryCode = form.cleaned_data["countryCode"]
            nationality = form.cleaned_data["nationality"]
            surname = form.cleaned_data["surname"]
            gender = form.cleaned_data["gender"]
            dob = form.cleaned_data["dob"]
            placeOfBirth = form.cleaned_data["placeOfBirth"]
            placeOfIssue = form.cleaned_data["placeOfIssue"]
            dateOfIssue = form.cleaned_data["dateOfIssue"]
            dateOfExpiry = form.cleaned_data["dateOfExpiry"]
            faceId = request.FILES.get("faceId")
            sign = request.FILES.get("sign")
            father = form.cleaned_data["father"]
            mother = form.cleaned_data["mother"]
            spouse = form.cleaned_data["spouse"]
            address_1 = form.cleaned_data["address_1"]
            address_2 = form.cleaned_data["address_2"]
            address_3 = form.cleaned_data["address_3"]
            oldPassNum = form.cleaned_data["oldPassNum"]
            oldPlaceIssue = form.cleaned_data["oldPlaceIssue"]
            oldDateIssue = form.cleaned_data["oldDateIssue"]
            fileNum = form.cleaned_data["fileNum"]

            faceIdHash = upload_image(faceId.name, faceId.read())
            signIdHash = upload_image(sign.name, sign.read())
            oldPassNumDateAndIssue = (
                oldPassNum + " " + str(oldDateIssue) + " " + oldPlaceIssue
            )
            address = address_1 + ";" + address_2 + ";" + address_3

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

            resp = new_passport(
                passnum=passNum,
                personal_info=personal_info,
                imagesInfo=imagesInfo,
                passportInfo=passportInfo,
            )

            if resp["success"]:
                request.session["my_messages"] = {
                    "success": True,
                    "message": "Passport Uploaded Successfully",
                }
            elif (
                str(resp)
                == "{'success': False, 'data': ContractLogicError('execution reverted: Passport Already Exists!')}"
            ):
                request.session["my_messages"] = {
                    "warning": True,
                    "message": "Passport Already Exists",
                }
            else:
                request.session["my_messages"] = {
                    "error": True,
                    "message": "Oops, Something went wrong",
                }
            return redirect("main:home")
        else:
            return render(request, "uploadPage.html", {"form": form})


class updatePageInitial(View):
    @redirector("update")
    def get(self, request, *args, **kwargs):
        pass


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
