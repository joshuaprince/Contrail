from django.urls import path
from django.conf.urls.static import static

from contrail.frontend.settings import settings
from .views import *

urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('price/', price_view, name='price'),
    path('instance/', instance_view, name='instance'),
    path('historygraph/', history_graph_view, name='historygraph'),
    path('help/', HelpView.as_view(), name='help'),

] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
