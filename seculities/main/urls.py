from django.conf.urls import url
from . import views
from django.urls import include, path



urlpatterns = [
    path('top/', views.top, name='top'),
    path('upload', views.upload, name='upload'),
    path('upload_complete', views.upload_complete, name='upload_complete'),
]
