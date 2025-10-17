from django.contrib import admin
from django.urls import path, include, re_path
from django.views.generic import TemplateView
from django.contrib.auth.decorators import login_required
from django.conf import settings
from django.views.static import serve as static_serve
from rest_framework.routers import DefaultRouter

from core.views import PatientViewSet, AttachmentViewSet, health, storage_diag, echo_diag

router = DefaultRouter()
router.register(r'patients', PatientViewSet, basename='patient')
router.register(r'attachments', AttachmentViewSet, basename='attachment')

urlpatterns = [
    path('admin/', admin.site.urls),
    path('v1/', include(router.urls)),
    path('accounts/', include('django.contrib.auth.urls')),

    # Front
    path('', TemplateView.as_view(template_name='public/index.html'), name='public_form'),
    path('gracias.html', TemplateView.as_view(template_name='public/gracias.html'), name='gracias'),
    path('panel/', login_required(TemplateView.as_view(template_name='panel/index.html')), name='panel'),

    # Health / Diag
    path('health/', health, name='health'),
    path('diag/storage/', storage_diag, name='storage_diag'),
    path('diag/echo/', echo_diag, name='echo_diag'),

    # SERVIR MEDIA SIEMPRE (hotfix)
    re_path(r'^media/(?P<path>.*)$', static_serve, {'document_root': settings.MEDIA_ROOT}),
]
