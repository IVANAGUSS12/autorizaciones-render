from rest_framework import viewsets, permissions
from rest_framework.parsers import MultiPartParser, FormParser
from .models import Patient, Attachment
from .serializers import PatientSerializer, AttachmentSerializer
from django.http import JsonResponse

class PatientViewSet(viewsets.ModelViewSet):
    queryset = Patient.objects.all().order_by("-created_at")
    serializer_class = PatientSerializer
    parser_classes = [MultiPartParser, FormParser]

    # público puede CREAR (para el QR). El resto autenticado.
    def get_permissions(self):
        if self.action in ["create"]:
            return [permissions.AllowAny()]
        return [permissions.IsAuthenticated()]

class AttachmentViewSet(viewsets.ModelViewSet):
    queryset = Attachment.objects.select_related("patient").order_by("-created_at")
    serializer_class = AttachmentSerializer
    parser_classes = [MultiPartParser, FormParser]

    def get_permissions(self):
        if self.action in ["create"]:
            return [permissions.AllowAny()]
        return [permissions.IsAuthenticated()]
# core/views.py (añadir al final)

    def health(request):
    return JsonResponse({"status": "ok"})
