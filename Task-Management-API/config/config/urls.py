from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework.authtoken.views import obtain_auth_token

from tasks.views import TaskViewSet, task_list, task_create, task_toggle, task_delete
from accounts.views import register_page, login_page, logout_view, RegisterView

router = DefaultRouter()
router.register(r'tasks', TaskViewSet)

urlpatterns = [
    path('admin/', admin.site.urls),

    path('api/', include(router.urls)),
    path('api/register/', RegisterView.as_view(), name='api_register'),
    path('api-token-auth/', obtain_auth_token, name='api_token_auth'),

    path('', task_list, name='task_list'),
    path('add/', task_create, name='task_create'),
    path('toggle/<int:pk>/', task_toggle, name='task_toggle'),

    path('register/', register_page, name='register'),
    path('login/', login_page, name='login'),
    path('logout/', logout_view, name='logout'),
    path('delete/<int:pk>/', task_delete, name='task_delete'),
]
