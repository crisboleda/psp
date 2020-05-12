
# Django
from django.urls import path
from django.contrib.auth.views import LogoutView

# Views
from users.views import (LoginUserView, UserProfileView, update_experencie_languages, 
                        UpdateImageProfile, DeleteImageProfile, RegisterUserView)


urlpatterns = [

    path('login/', LoginUserView.as_view(), name='login'),
    path('register/', RegisterUserView.as_view(), name='register'),
    path('logout/', LogoutView.as_view(), name='logout'),

    path('<str:slug>/profile/', UserProfileView.as_view(), name='profile_user'),
    path('update/languages/', update_experencie_languages, name='update_languages'),
    path('profile/<int:pk>/', UpdateImageProfile.as_view(), name='update_image_profile'),
    path('profile/<int:pk>/delete/', DeleteImageProfile.as_view(), name='delete_image_profile')
]


