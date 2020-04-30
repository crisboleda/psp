
# Django
from django.urls import path
from django.contrib.auth.views import LogoutView

# Views
from users.views import LoginUserView, ProfileUserView, UserProfileView


urlpatterns = [

    path('login/', LoginUserView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('<str:slug>/profile/', UserProfileView.as_view(), name='profile_user')

]


