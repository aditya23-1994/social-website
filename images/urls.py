from django.conf.urls import url
from . import views
app_name = 'images'
urlpatterns = [
    url(r'^created/$', views.image_create, name='create'),
]