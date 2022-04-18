from .views import homepage, uploadPage, verifyPage, loginView, logoutView
from django.urls import path
urlpatterns = [
    path("", homepage.as_view(), name = 'home'),
    path("upload", uploadPage.as_view(), name="uploadPage"),
    path("verify", verifyPage.as_view(), name="verifyPage"),
    path("login", loginView.as_view(), name="loginView"),
    path("logout", logoutView.as_view(), name="logoutView")
]

