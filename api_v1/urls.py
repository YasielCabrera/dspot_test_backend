from django.urls import include, path, re_path
from rest_framework import routers, permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

from .profile import views as profile_views


schema_view = get_schema_view(
    openapi.Info(
        title="DSpot test",
        default_version='v1',
        description="DSpot Full Stack test API",
        contact=openapi.Contact(email="contact@dspot.com.pl"),
        license=openapi.License(name="BSD License"),
    ),
    public=True,
    permission_classes=[permissions.AllowAny],
)

router = routers.DefaultRouter()
router.register(r'profile', profile_views.ProfileViewSet)
router.register(r'friends', profile_views.FriendView, basename='friend')

urlpatterns = [
    path('', include(router.urls)),
    # path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    re_path(r'^swagger(?P<format>\.json|\.yaml)$',
            schema_view.without_ui(cache_timeout=0), name='schema-json'),
    re_path(r'^swagger/$', schema_view.with_ui('swagger',
            cache_timeout=0), name='schema-swagger-ui'),
    re_path(r'^redoc/$', schema_view.with_ui('redoc',
            cache_timeout=0), name='schema-redoc'),
]
