from django.shortcuts import render, redirect
from django.views.generic import View
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import User
import datetime
from django.conf import settings
import os
import io
import base64
from PIL import Image
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
    @cleanup
    def get(self, request, *args, **kwargs):
        logout(request)
        request.session["my_messages"] = {
            "success": True,
            "message": "Logged Out Successfully",
        }
        return redirect("main:loginView")


class homepage(View):
    @redirector("home")
    @cleanup
    def get(self, request, *args, **kwargs):
        if "my_messages" in request.session:
            my_messages = request.session["my_messages"]
            del request.session["my_messages"]
            return render(request, "home.html", {"my_messages": my_messages})
        return render(request, "home.html")


class uploadPage(View):
    @redirector("upload")
    @cleanup
    def get(self, request, *args, **kwargs):
        form = passportDataForm()
        return render(request, "uploadPage.html", {"form": form})

    @redirector("upload")
    @cleanup
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
            spouse = (
                "" if not form.cleaned_data["spouse"] else form.cleaned_data["spouse"]
            )
            address_1 = form.cleaned_data["address_1"]
            address_2 = form.cleaned_data["address_2"]
            address_3 = form.cleaned_data["address_3"]
            oldPassNum = (
                ""
                if not form.cleaned_data["oldPassNum"]
                else form.cleaned_data["oldPassNum"]
            )
            oldPlaceIssue = (
                ""
                if not form.cleaned_data["oldPlaceIssue"]
                else form.cleaned_data["oldPlaceIssue"]
            )
            oldDateIssue = (
                ""
                if not form.cleaned_data["oldDateIssue"]
                else form.cleaned_data["oldDateIssue"]
            )
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
    @cleanup
    def get(self, request, *args, **kwargs):
        form = passportNumberForm()
        if "my_messages" in request.session:
            my_messages = request.session["my_messages"]
            del request.session["my_messages"]
            return render(
                request,
                "updatePageInitial.html",
                {"form": form, "my_messages": my_messages},
            )
        return render(request, "updatePageInitial.html", {"form": form})

    @redirector("update")
    @cleanup
    def post(self, request, *args, **kwargs):
        form = passportNumberForm(request.POST)
        if form.is_valid():
            resp = get_passport_details(form.cleaned_data["passNum"])
            if not resp["success"]:
                if resp["data"] == "Passport Hasn't Been Uploaded":
                    request.session["my_messages"] = {
                        "warning": True,
                        "message": "Passport Hasn't Been Uploaded",
                    }
                else:
                    request.session["my_messages"] = {
                        "error": True,
                        "message": "Oops, Something went wrong",
                    }
                return redirect("main:updatePageInitial")
            else:
                request.session["passportData"] = resp["data"]
                return redirect("main:updatePage")
        else:
            return render(request, "updatePageInitial.html", {"form": form})


class updatePage(View):
    @redirector("update")
    def get(self, request, *args, **kwargs):
        if "passportData" not in request.session:
            return redirect("main:updatePageInitial")
        details = request.session["passportData"]
        address_split = details[10].split(";")
        oldPassData_split = details[18].split(" ")
        data = {
            "surname": details[1],
            "holderName": details[2],
            "nationality": details[3],
            "gender": details[4],
            "dob": datetime.datetime.strptime(details[5], "%Y-%m-%d"),
            "placeOfBirth": details[6],
            "father": details[7],
            "mother": details[8],
            "spouse": details[9],
            "address_1": address_split[0],
            "address_2": address_split[1],
            "address_3": address_split[2],
            "type": details[13],
            "countryCode": details[14],
            "placeOfIssue": details[15],
            "dateOfIssue": datetime.datetime.strptime(details[16], "%Y-%m-%d"),
            "dateOfExpiry": datetime.datetime.strptime(details[17], "%Y-%m-%d"),
            "oldPassNum": oldPassData_split[0],
            "oldPlaceIssue": oldPassData_split[1],
            "oldDateIssue": datetime.datetime.strptime(oldPassData_split[2], "%Y-%m-%d")
            if oldPassData_split[2] != ""
            else "",
            "fileNum": details[19],
        }
        form = passportDataForm(data)
        form.fields["passNum"].initial = details[0]
        form.fields["passNum"].disabled = True
        form.fields["faceId"].required = False
        form.fields["sign"].required = False
        images = [download_image(details[11]), download_image(details[12])]
        username = request.user.get_username()
        FaceId = Image.open(io.BytesIO(base64.b64decode(images[0])))
        FaceId.save(
            os.path.join(settings.BASE_DIR, "media", username + "FaceId.png"), "png"
        )
        FaceId.close()
        Sign = Image.open(io.BytesIO(base64.b64decode(images[1])))
        Sign.save(
            os.path.join(settings.BASE_DIR, "media", username + "Sign.png"), "png"
        )
        Sign.close()
        images_url = [
            "/media/" + username + "FaceId.png",
            "/media/" + username + "Sign.png",
        ]
        return render(request, "updatePage.html", {"form": form, "images": images_url})

    @redirector("update")
    def post(self, request, *args, **kwargs):
        if "passportData" not in request.session:
            return redirect("main:updatePageInitial")
        if request.FILES:
            form = passportDataForm(request.POST, request.FILES)
        else:
            form = passportDataForm(request.POST)
        form.fields["passNum"].initial = request.session["passportData"][0]
        form.fields["passNum"].disabled = True
        form.fields["faceId"].required = False
        form.fields["sign"].required = False
        if form.is_valid():
            typeOfPass = form.cleaned_data["type"]
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
            spouse = (
                "" if not form.cleaned_data["spouse"] else form.cleaned_data["spouse"]
            )
            address_1 = form.cleaned_data["address_1"]
            address_2 = form.cleaned_data["address_2"]
            address_3 = form.cleaned_data["address_3"]
            oldPassNum = (
                ""
                if not form.cleaned_data["oldPassNum"]
                else form.cleaned_data["oldPassNum"]
            )
            oldPlaceIssue = (
                ""
                if not form.cleaned_data["oldPlaceIssue"]
                else form.cleaned_data["oldPlaceIssue"]
            )
            oldDateIssue = (
                ""
                if not form.cleaned_data["oldDateIssue"]
                else form.cleaned_data["oldDateIssue"]
            )
            fileNum = form.cleaned_data["fileNum"]
            if form.cleaned_data["faceId"]:
                faceIdHash = upload_image(faceId.name, faceId.read())
            else:
                faceIdHash = request.session["passportData"][11]
            if form.cleaned_data["sign"]:
                signIdHash = upload_image(sign.name, sign.read())
            else:
                signIdHash = request.session["passportData"][12]
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

            resp = update_passport_details(
                passnum=request.session["passportData"][0],
                personalInfo=personal_info,
                imagesInfo=imagesInfo,
                passportInfo=passportInfo,
            )

            if resp["success"]:
                request.session["my_messages"] = {
                    "success": True,
                    "message": "Passport Updated Successfully",
                }
            else:
                request.session["my_messages"] = {
                    "error": True,
                    "message": "Oops, Something went wrong",
                }
            del request.session["passportData"]
            username = request.user.get_username()
            os.remove(os.path.join(settings.BASE_DIR, "media", username + "FaceId.png"))
            os.remove(os.path.join(settings.BASE_DIR, "media", username + "Sign.png"))
            return redirect("main:home")
        else:
            username = request.user.get_username()
            images_url = [
                "/media/" + username + "FaceId.png",
                "/media/" + username + "Sign.png",
            ]
            return render(
                request, "updatePage.html", {"form": form, "images": images_url}
            )


class verifyPage(View):
    @redirector("verify")
    def get(self, request, *args, **kwargs):
        return render(request, "verifyPage.html", context={"get_details": False})

    @redirector("verify")
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
