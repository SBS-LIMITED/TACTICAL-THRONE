from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('login', views.login, name='login'),
    path('signup', views.signup, name='signup'),
    path('about', views.about, name='about'),
    path('userboard', views.userboard, name='userboard'),
    path('feedback', views.feedback, name='feedback'),
    path('settings', views.settings, name='settings'),
    path('update/<str:email>', views.update, name='update'),
    path('invite', views.invite, name='invite'),
    path('gamecode', views.gamecode, name='gamecode'),
    
]
