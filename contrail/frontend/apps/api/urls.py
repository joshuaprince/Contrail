from django.urls import include, path
from .views import *

urlpatterns = [
    path('getinstances/', GetInstances.as_view(), name='getinstances'),
    path('getinstancedetail/', GetInstanceDetail.as_view(), name='getinstancedetail'),
    path('getinstancepricehistory/', GetInstancePriceHistory.as_view(), name='getinstancepricehistory'),
]
