from .views import *
from django.urls import path

app_name = "main"

urlpatterns = [
    path("", homepage.as_view(), name="home"),
    path("upload", uploadPage.as_view(), name="uploadPage"),
    path("update", updatePageInitial.as_view(), name="updatePageInitial"),
    path("update/edit", updatePage.as_view(), name="updatePage"),
    path("verify", verifyPage.as_view(), name="verifyPage"),
    path("login", loginView.as_view(), name="loginView"),
    path("logout", logoutView.as_view(), name="logoutView"),
]
