from django.urls import path

from . import views

urlpatterns = [
    path('', views.main_page, name='main_page'),
    path('recruit', views.recruit, name='recruit'),
    path('sith', views.sith, name='sith'),
    path('sithinfo', views.sithinfo, name='sithinfo'),

]
