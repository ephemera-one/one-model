from api.views import GeneratorTaskViewSet
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path
from rest_framework import routers

api_router = routers.DefaultRouter()
api_router.register(r"tasks", GeneratorTaskViewSet)

urlpatterns = [
    path("api/", include(api_router.urls)),
    path("admin/", admin.site.urls),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
