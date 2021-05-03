from django.urls import path
from . import views

app_name = ""

urlpatterns = [
    path('index/', views.index, name="index"),
    path('', views.test, name='introduce'),
    path('register/', views.registerPage, name='register'),
    path('login/', views.loginPage, name='login'),
    path('logout/', views.logoutUser, name='logout'),
    path('songs/', views.songs, name='songs'),
    path('songs/<int:id>/', views.songpost, name='songpost'),
]
