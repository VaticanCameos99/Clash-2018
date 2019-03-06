from django.urls import path, re_path
from . import views
from django.contrib.auth import login, logout
from django.views.generic import DetailView

urlpatterns = [

    path('add/', views.addq),
    path('display/', views.display),
    path('', views.home),
    path('logout/', views.loggedout),
    path('register/',views.register, name='register'),
    path('rules/', views.rules),
    path('skipurl1/', views.skip),
    path('anscheck/',views.anscheck, name='anscheck'),
    #path('perception/',views.perception),
    path('timer/', views.timer),
    path('validate_username/', views.validate_username),
    path('perception_check/', views.perception_check),
    path('loggedin/', views.logged),
    path('addq/', views.addq),
    re_path(r'/', views.register),
    
]

