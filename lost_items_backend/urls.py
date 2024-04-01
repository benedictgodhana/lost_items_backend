"""
URL configuration for lost_items_backend project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from . import views
from .views import csrf_token
from .views import register
from .views import registered_users
from .views import logout_view


urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('lostitems.urls')),  # Include lostitems app URLs
    path('api/', include('users.urls')),      # Include users app URLs
    path('api/login/', views.login, name='login'),
    path('api/logout/', logout_view, name='logout'),
    path('api/register/', register, name='register'),
    path('api/csrf/', csrf_token, name='csrf_token'),  # Define the URL pattern for /api/csrf
    path('api/registered-users/', registered_users, name='registered-users'),
    path('api/user_count/', views.user_count, name='user-count'),
    path('api/claim/', views.claim_lost_item, name='claim-lost-item'),
    
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
