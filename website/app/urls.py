from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('tasks/', views.tasks, name='tasks'),
    path('task/<str:pk>', views.task, name='task'),
    path('offer/<str:pk>', views.offer, name='offer'),
    path('makeoffer/<str:pk>', views.makeoffer, name='makeoffer'),
    path('create/', views.create, name='create'),
    path('main/', views.main, name='main'),
    path('staff/', views.stuff, name='stuff'),
    path('profile/<str:pk>', views.profile, name='profile'),
    path('become/', views.become, name='become'),
    path('login/', views.loginPage, name='login'),
    path('logout/', views.logoutUser, name='logout'),
    path('register/', views.registerPage, name='register'),
    path('update-user/', views.updateUser , name="update-user"),
    path('ajax/load-list/', views.loadList, name='load-list')    
]