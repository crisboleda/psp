
# Django
from django.urls import path
from django.contrib.auth.views import LogoutView

# Views
from users.views import LoginUserView, ProfileUserView


urlpatterns = [

    path('login/', LoginUserView.as_view(), name='login'),
    path('<str:slug>/profile/', ProfileUserView.as_view(), name='profile_user'),
    path('logout/', LogoutView.as_view(), name='logout'),

]


