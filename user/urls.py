from django.urls import path
from user.views import SignupView, LoginUserView, GetEditProfile, UpdatePasswordView, auth_oauth2

urlpatterns = [

    path('signup', SignupView.as_view()),
    path('', auth_oauth2),
    path('login', LoginUserView.as_view()),
    path('profile', GetEditProfile.as_view()),
    path('update_password', UpdatePasswordView.as_view()),
]
