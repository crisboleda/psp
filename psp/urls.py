
# Django
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.shortcuts import render

# Views
from psp.views import DashboardView, IndexView, HomeView, DashboardConfigurationView
from users.views import CalendarAdminView, DateDeliveryView

# Libraries
from decouple import config


urlpatterns = [
    path('admin/', admin.site.urls),
    path('home/', HomeView.as_view(), name='dashboard'),

    path('i18n/', include('django.conf.urls.i18n')),
    path('settings/', DashboardConfigurationView.as_view(), name='configuration'),

    path('', IndexView.as_view(), name='index'),
    
    # Calendar Admin
    path('calendar/', CalendarAdminView.as_view(), name='calendar'),
    path('dates-delivery/', DateDeliveryView.as_view(), name='date_delivery'),
    
    # URL APP users
    path('users/', include(('users.urls', 'users'), namespace='users')),
    
    # URL APP projects
    path('projects/', include(('projects.urls', 'projects'), namespace='projects')),

    # URL APP Programs
    path('', include(('programs.urls', 'programs'), namespace='programs')),

    # URL APP Logs
    path('', include(('logs.urls', 'logs'), namespace='logs')),

]

if not config('DJANGO_PRODUCTION_ENV', default=False, cast=bool):
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

