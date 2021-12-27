from django.contrib import admin
from django.urls import path, include
from rest_framework.authtoken import views as rest_auth_views
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from authapp.views import UserModelViewSet
from todoapp.views import ProjectModelViewSet, TodoModelViewSet

router = DefaultRouter()
router.register('users', UserModelViewSet)
router.register('projects', ProjectModelViewSet)
router.register('todos', TodoModelViewSet)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api-auth/', include('rest_framework.urls')),
    path('api/', include(router.urls)),
    path('api-token-auth/', rest_auth_views.obtain_auth_token),
    path('api-jwt-token/', TokenObtainPairView.as_view()),
    path('api-jwt-token/refresh/', TokenRefreshView.as_view()),
]
