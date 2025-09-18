from django.urls import path
from . import views
from rest_framework.authtoken.views import obtain_auth_token

urlpatterns = [
    path("register/",views.CreateUserView.as_view(),name="register"),
    path("auth-token/",obtain_auth_token,name="obtain-auth-token")
]