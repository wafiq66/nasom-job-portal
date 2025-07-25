"""
URL configuration for nasom_job_portal project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
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
from django.contrib.auth import views as auth_views
from django.conf import settings
from django.conf.urls.static import static  # <- important!

urlpatterns = [
    path('admin/', admin.site.urls),
    path('',include('register_page.urls')),
    path('',include('login_page.urls')),
    path('',include('landing_page.urls')),
    path('',include('profile_user.urls')),
    path('',include('my_job_ad.urls')),
    path('',include('my_job_list.urls')),
    path('',include('manage_applicant.urls')),
    path('',include('verify_applicant.urls')),
    path('logout/', auth_views.LogoutView.as_view(next_page='landing_applicant'), name='logout'),
]

# 🔥 This goes at the bottom, outside urlpatterns[]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
