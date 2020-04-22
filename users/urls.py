
# Django
from django.urls import path

# Views
from users.views import LoginView


urlpatterns = [
    path('login/', LoginView.as_view(), name='login_user')
]


