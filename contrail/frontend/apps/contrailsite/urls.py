from django.urls import path
from django.conf.urls.static import static

from .views import *

urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('price/', priceview, name='price'),
    path('instance/', instanceview, name='instance'),
    path('help/', HelpView.as_view(), name='help'),

] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
