from django.contrib import admin
from django.urls import path, include
from django.views.generic import TemplateView
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth.decorators import login_required

from rest_framework.routers import DefaultRouter
from core.views import PatientViewSet, AttachmentViewSet, health

router = DefaultRouter()
router.register(r'patients', PatientViewSet, basename='patient')
router.register(r'attachments', AttachmentViewSet, basename='attachment')

urlpatterns = [
    path('admin/', admin.site.urls),
    path('v1/', include(router.urls)),
    path('accounts/', include('django.contrib.auth.urls')),

    path('', TemplateView.as_view(template_name='public/index.html'), name='public_form'),
    path('gracias.html', TemplateView.as_view(template_name='public/gracias.html'), name='gracias'),
    path('panel/', login_required(TemplateView.as_view(template_name='panel/index.html')), name='panel_index'),

    # Health check para DigitalOcean
    path('health/', health, name='health_check'),
]

# Solo en desarrollo local cuando USE_S3=False y DEBUG=True
if settings.DEBUG and not settings.USE_S3:
    urlpatterns += static(settings.MEDIA_URL, document_root=getattr(settings, "MEDIA_ROOT", None))
