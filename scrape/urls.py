from django.urls import path
from . import views
import uuid

app_name = 'scrape'

urlpatterns = [
    # path('', views.index, name = 'home',)
    path('', views.GetDate.as_view(), name = 'home'),
    path("download/<uuid:uuid>/",views.downloader, name = 'downloader')
]
