from rest_framework import viewsets, permissions
from rest_framework.parsers import MultiPartParser, FormParser

from .models import Patient, Attachment
from .serializers import PatientSerializer, AttachmentSerializer

class CreateIsOpenOtherwiseAuth(permissions.BasePermission):
    """Allow Any for POST (create). Require authenticated for other methods."""
    def has_permission(self, request, view):
        if request.method == "POST":
            return True
        return request.user and request.user.is_authenticated

class PatientViewSet(viewsets.ModelViewSet):
    queryset = Patient.objects.all().order_by("-created_at")
    serializer_class = PatientSerializer
    permission_classes = [CreateIsOpenOtherwiseAuth]

    def get_queryset(self):
        qs = super().get_queryset()
        cobertura = self.request.query_params.get("cobertura")
        estado = self.request.query_params.get("estado")
        medico = self.request.query_params.get("medico")
        sector_code = self.request.query_params.get("sector__code") or self.request.query_params.get("sector")
        if cobertura: qs = qs.filter(cobertura=cobertura)
        if estado: qs = qs.filter(estado=estado)
        if medico: qs = qs.filter(medico=medico)
        if sector_code: qs = qs.filter(sector_code=sector_code)
        return qs

class AttachmentViewSet(viewsets.ModelViewSet):
    queryset = Attachment.objects.all().order_by("-created_at")
    serializer_class = AttachmentSerializer
    parser_classes = [MultiPartParser, FormParser]
    permission_classes = [CreateIsOpenOtherwiseAuth]
