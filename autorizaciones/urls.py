from django.contrib import admin
from django.urls import path, include
from django.views.generic import TemplateView
from django.contrib.auth.decorators import login_required
from django.conf import settings
from django.conf.urls.static import static

from rest_framework.routers import DefaultRouter
from core.views import PatientViewSet, AttachmentViewSet

router = DefaultRouter()
router.register(r"patients", PatientViewSet, basename="patient")
router.register(r"attachments", AttachmentViewSet, basename="attachment")

urlpatterns = [
    path("admin/", admin.site.urls),

    # API
    path("v1/", include(router.urls)),
    path("api-auth/", include("rest_framework.urls")),  # login/logout en la UI del DRF

    # Auth
    path("accounts/", include("django.contrib.auth.urls")),

    # Público
    path("", TemplateView.as_view(template_name="public/index.html"), name="public_form"),
    path("gracias.html", TemplateView.as_view(template_name="public/gracias.html"), name="gracias"),

    # Panel interno (requiere login)
    path("panel/", login_required(TemplateView.as_view(template_name="panel/index.html")), name="panel_index"),
]

# Servir /media/ también en prod (temporal hasta usar Spaces/S3)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
