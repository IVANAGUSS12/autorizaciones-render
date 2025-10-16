from rest_framework import viewsets, permissions
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.authentication import SessionAuthentication
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

from .models import Patient, Attachment
from .serializers import PatientSerializer, AttachmentSerializer

# --- Auth helper: exentar CSRF solo cuando lo indiquemos ---
class CsrfExemptSessionAuthentication(SessionAuthentication):
    def enforce_csrf(self, request):
        return  # desactiva verificación CSRF

class PatientViewSet(viewsets.ModelViewSet):
    queryset = Patient.objects.all().order_by("-created_at")
    serializer_class = PatientSerializer
    parser_classes = [MultiPartParser, FormParser]

    def get_permissions(self):
        # Público puede CREAR desde el formulario QR
        if self.action in ["create"]:
            return [permissions.AllowAny()]
        return [permissions.IsAuthenticated()]

    def get_authenticators(self):
        # Exentamos CSRF SOLO para create (POST público)
        if self.action in ["create"]:
            return [CsrfExemptSessionAuthentication()]
        return [SessionAuthentication()]

class AttachmentViewSet(viewsets.ModelViewSet):
    queryset = Attachment.objects.select_related("patient").order_by("-created_at")
    serializer_class = AttachmentSerializer
    parser_classes = [MultiPartParser, FormParser]

    def get_permissions(self):
        if self.action in ["create"]:
            return [permissions.AllowAny()]
        return [permissions.IsAuthenticated()]

    def get_authenticators(self):
        if self.action in ["create"]:
            return [CsrfExemptSessionAuthentication()]
        return [SessionAuthentication()]

# ---------------------------------------------------------
# Health check para DigitalOcean
# ---------------------------------------------------------
@csrf_exempt
def health(request):
    return JsonResponse({"status": "ok"})
