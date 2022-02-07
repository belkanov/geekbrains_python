from django.contrib import admin
from django.urls import path, include, re_path
from rest_framework import permissions
from rest_framework.authtoken import views as rest_auth_views
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

from authapp.views import UserModelViewSet
from todoapp.views import ProjectModelViewSet, TodoModelViewSet

router = DefaultRouter()
router.register('users', UserModelViewSet)
router.register('projects', ProjectModelViewSet)
router.register('todos', TodoModelViewSet)

schema_view = get_schema_view(
    openapi.Info(
        title='TODOs',
        default_version='1.0',
        description="Docs to TODOs' project",
        contact=openapi.Contact(email='test@example.com'),
        license=openapi.License(name='MIT License'),
    ),
    public=True,
    permission_classes=(permissions.AllowAny, )
)

urlpatterns = [
    path('admin/', admin.site.urls),

    path('api/', include(router.urls)),

    path('api-auth/', include('rest_framework.urls')),
    path('api-token-auth/', rest_auth_views.obtain_auth_token),
    # path('api-jwt-token/', TokenObtainPairView.as_view()),
    # path('api-jwt-token/refresh/', TokenRefreshView.as_view()),

    re_path(r'^swagger(?P<format>\.json|\.yaml)$', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
]
