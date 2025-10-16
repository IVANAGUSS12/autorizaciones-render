from rest_framework import viewsets, permissions, status
from rest_framework.parsers import MultiPartParser, FormParser, JSONParser
from rest_framework.response import Response
from django.http import JsonResponse
from .models import Patient, Attachment
from .serializers import PatientSerializer, AttachmentSerializer
import logging

logger = logging.getLogger(__name__)

class PatientViewSet(viewsets.ModelViewSet):
    queryset = Patient.objects.all().order_by("-created_at")
    serializer_class = PatientSerializer
    parser_classes = [MultiPartParser, FormParser, JSONParser]

    def get_permissions(self):
        if self.action == "create":
            return [permissions.AllowAny()]
        return [permissions.IsAuthenticated()]

    def create(self, request, *args, **kwargs):
        try:
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            patient = serializer.save()
            return Response(PatientSerializer(patient).data, status=status.HTTP_201_CREATED)
        except Exception as e:
            logger.error(f"Error creando paciente: {e}")
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

class AttachmentViewSet(viewsets.ModelViewSet):
    queryset = Attachment.objects.all().order_by("-created_at")
    serializer_class = AttachmentSerializer
    parser_classes = [MultiPartParser, FormParser, JSONParser]

    def get_permissions(self):
        if self.action == "create":
            return [permissions.AllowAny()]
        return [permissions.IsAuthenticated()]

def health(request):
    return JsonResponse({"status": "ok"})


