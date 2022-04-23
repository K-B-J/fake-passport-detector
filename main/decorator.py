from django.shortcuts import redirect


def redirector(page):
    def decorator(func):
        def logic(self, request, *args, **kwargs):
            if request.user.get_username() == "":
                return redirect("main:loginView")
            elif page in ["verify", "report"] and (
                "verifier" not in request.session and not request.user.is_superuser
            ):
                return redirect("main:home")
            elif page in ["upload", "update", "home"] and (
                "issuer" not in request.session and not request.user.is_superuser
            ):
                return redirect("main:verifyPageInitial")
            else:
                return func(self, request, *args, **kwargs)

        return logic

    return decorator
