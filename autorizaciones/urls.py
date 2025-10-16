from django.contrib import admin
from django.urls import path, include, re_path
from django.views.generic import TemplateView
from django.conf import settings
from django.views.static import serve

from rest_framework.routers import DefaultRouter
from core.views import PatientViewSet, AttachmentViewSet

router = DefaultRouter()
router.register(r'patients', PatientViewSet, basename='patient')
router.register(r'attachments', AttachmentViewSet, basename='attachment')

urlpatterns = [
    path('admin/', admin.site.urls),
    path('v1/', include(router.urls)),
    path('accounts/', include('django.contrib.auth.urls')),
    path('', TemplateView.as_view(template_name='public/index.html'), name='public_form'),
    path('gracias.html', TemplateView.as_view(template_name='public/gracias.html'), name='gracias'),
    path('panel/', TemplateView.as_view(template_name='panel/index.html'), name='panel_index'),
]

# ---------- FIX: servir archivos subidos ----------
urlpatterns += [
    re_path(r'^media/(?P<path>.*)$', serve, {'document_root': settings.MEDIA_ROOT}),
]
