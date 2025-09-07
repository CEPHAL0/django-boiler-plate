from django.contrib import admin
from django.urls import path, include
from drf_yasg.views import get_schema_view
from rest_framework import permissions
from drf_yasg import openapi
from django.http import JsonResponse
from rest_framework import status
from rest_framework.status import HTTP_404_NOT_FOUND, HTTP_500_INTERNAL_SERVER_ERROR

from tenants.urls import tenant_urlpatterns, tenant_user_urlpatterns

schema_view = get_schema_view(
    openapi.Info(
        title = 'Snippets API',
        default_version='v1',
        description='Test description',
        license=openapi.License(name="TOS")
    ),
    public=True,
    permission_classes=[permissions.AllowAny,],
)

# Register custom handlers
def custom_404_handler(request, exception):
    return JsonResponse({
        "status": "Failed",
        "status_code": status.HTTP_404_NOT_FOUND,
        "message": "Resource not found",
        "data": {}
    }, status=HTTP_404_NOT_FOUND)



def custom_500_handler(request):
    return JsonResponse({
        "status": "Failed",
        "status_code": status.HTTP_500_INTERNAL_SERVER_ERROR,
        "message": "An unexpected error occurred",
        "data": {}
    }, status=HTTP_500_INTERNAL_SERVER_ERROR)


handler404 = custom_404_handler
handler500 = custom_500_handler


urlpatterns = [
    path('admin/', admin.site.urls),
    path('swagger/<format>', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    path('swagger', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
    path('users/', include('users.urls')),
    path('tenants/', include('tenants.urls')),
    path('conferences/', include('conferences.urls')),
]
