from django.conf.urls import url
from django.urls import path,include,re_path
from rest_framework import routers
from . import views

app_name = 's3file_app'

router = routers.DefaultRouter()
router.register(r'',views.S3FileViewSet)

urlpatterns = [
    url(r'^',include(router.urls)),
    url(r'^api-auth/', include('rest_framework.urls',namespace='rest_framework')),
]