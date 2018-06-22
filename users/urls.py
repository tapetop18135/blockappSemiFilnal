from django.urls import path
from . import views

app_name = 'usersapp'

urlpatterns = [
    path('signin', views.SignIn.as_view() ,name="signin"),
    path('signup', views.SignUp.as_view() ,name="signup"),
    path('signout', views.SignOut.as_view() ,name="signout")
]