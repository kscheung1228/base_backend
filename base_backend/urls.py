"""base_backend URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
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
# from django.contrib import admin
# from django.urls import path

# urlpatterns = [
#     path('admin/', admin.site.urls),
# ]

from django.conf.urls import url
from django.contrib import admin
from django.views.generic.base import TemplateView
from files.views import DownloadView, UploadView, UploadPolicyView
from django.urls import path,re_path,include
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
# from new_app.views import *

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    path ('s3files/',include('files.urls',namespace='api-files')),
    re_path(r'^files/(?P<id>\d+)/download/$', DownloadView.as_view()), # 2.0 +
    re_path(r'^upload/$', UploadView.as_view()), # 2.0 +
    re_path(r'^upload/policy/$', UploadPolicyView.as_view()), # 2.0 +
    url(r'^.*', TemplateView.as_view(template_name="home.html"), name="home"),
    url(r'^api/token/$', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    url(r'^api/token/refresh/$', TokenRefreshView.as_view(), name='token_refresh'),
]