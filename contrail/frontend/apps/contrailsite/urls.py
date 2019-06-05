from django.urls import path

from .views import *

urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('price/', price_view, name='price'),
    path('instance/', instance_view, name='instance'),
    path('historygraph/', history_graph_view, name='historygraph'),
    path('help/', HelpView.as_view(), name='help'),
    path('storage/', storage_view, name='storage'),
    path('aboutus/', AboutUs.as_view(), name='aboutus')
]
