from django.shortcuts import redirect
import os
from django.conf import settings


def redirector(page):
    def decorator(func):
        def logic(self, request, *args, **kwargs):
            if request.user.get_username() == "":
                return redirect("main:loginView")
            elif page in ["upload", "update"] and "verifier" in request.session:
                return redirect("main:home")
            elif page == "home" and "verifier" in request.session:
                return redirect("main:verifyPage")
            else:
                return func(self, request, *args, **kwargs)

        return logic

    return decorator


def cleanup(func):
    def logic(self, request, *args, **kwargs):
        if "passportData" in request.session:
            del request.session["passportData"]
        try:
            username = request.user.get_username()
            os.remove(os.path.join(settings.BASE_DIR, "media", username + "FaceId.png"))
            os.remove(os.path.join(settings.BASE_DIR, "media", username + "Sign.png"))
        except:
            pass
        return func(self, request, *args, **kwargs)

    return logic
