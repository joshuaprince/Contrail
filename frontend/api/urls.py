from django.urls import include, path
from rest_framework import routers
from .views import *

router = routers.DefaultRouter()
# router.register(r'data', DataViewSet, 'data')

urlpatterns = [
    path('', include(router.urls)),
    path('getinstances/', GetInstances.as_view(), name='data'),

]
