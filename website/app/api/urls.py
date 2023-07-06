from django.urls import path, include
from . import views 
from rest_framework import routers
from rest_framework.authtoken.views import obtain_auth_token

router = routers.DefaultRouter()
router.register(r'account', views.UserViewSet)
router.register(r'task', views.TaskViewSet)


urlpatterns = [
    path('', include(router.urls)),
    path('auth/', include('rest_framework.urls')),
    path('categories/', views.getCategories),
    path('subcategories/', views.getSubcategories),
    path('tasks/', views.getTasks),
    path('users/', views.getUsers),
    path('profile/', views.getProfile),
    path('my-profile/', views.getMyProfile),
    path('profile/<str:pk>/', views.getProfileOfUser),
    path('user-tasks/<str:pk>/', views.getTasksOfUser),
    path('register/', views.registerView.as_view()),
    path('login/', obtain_auth_token)
]

# urlpatterns = [
#     path('', views.getRoutes),
#     path('tasks/', views.getTasks),
#     path('tasks/<str:pk>', views.getTask),
#     path('login/', views.loginView.as_view()),
#     path('register/', views.registerView.as_view()),
# ]
