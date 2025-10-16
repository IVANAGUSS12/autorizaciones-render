from django.contrib import admin
from django.urls import path, include
from django.views.generic import TemplateView
from django.contrib.auth.decorators import login_required
from django.conf import settings
from django.conf.urls.static import static
from rest_framework.routers import DefaultRouter
from core.views import PatientViewSet, AttachmentViewSet, health

router = DefaultRouter()
router.register(r"patients", PatientViewSet)
router.register(r"attachments", AttachmentViewSet)

urlpatterns = [
    path("admin/", admin.site.urls),
    path("v1/", include(router.urls)),
    path("health/", health),
    path("accounts/", include("django.contrib.auth.urls")),
    path("", TemplateView.as_view(template_name="public/index.html")),
    path("gracias.html", TemplateView.as_view(template_name="public/gracias.html")),
    path("panel/", login_required(TemplateView.as_view(template_name="panel/index.html"))),
]

if settings.DEBUG and not settings.USE_S3:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
