from django.shortcuts import redirect


def redirector(page):
    def decorator(func):
        def logic(self, request, *args, **kwargs):
            if request.user.get_username() == "":
                return redirect("main:loginView")
            elif page in ["upload", "update"] and "verifier" in request.session:
                return redirect("main:home")
            else:
                return func(self, request, *args, **kwargs)

        return logic

    return decorator
