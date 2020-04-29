
# Django
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

# Views
from psp.views import DashboardView


urlpatterns = [
    path('admin/', admin.site.urls),
    path('dashboard/', DashboardView.as_view(), name='dashboard'),
    # URL APP users
    path('users/', include(('users.urls', 'users'), namespace='users'))

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
