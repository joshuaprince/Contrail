from django.urls import include, path
from rest_framework import routers
from .views import *

router = routers.DefaultRouter()

urlpatterns = [
    path('', include(router.urls)),
    path('getinstances/', GetInstances.as_view(), name='getinstances'),
    path('getinstancedetail/', GetInstanceDetail.as_view(), name='getinstancedetail'),
]
