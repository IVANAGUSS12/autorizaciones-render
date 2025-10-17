from rest_framework import viewsets, permissions, status
from rest_framework.parsers import MultiPartParser, FormParser, JSONParser
from rest_framework.response import Response
from django.http import JsonResponse

from .models import Patient, Attachment
from .serializers import PatientSerializer, AttachmentSerializer


class PublicReadCreatePermission(permissions.BasePermission):
    """
    Hotfix:
    - list, retrieve, create -> público
    - update, partial_update, destroy -> staff autenticado
    """
    def has_permission(self, request, view):
        if view.action in ["list", "retrieve", "create"]:
            return True
        return bool(request.user and request.user.is_authenticated and request.user.is_staff)


class PatientViewSet(viewsets.ModelViewSet):
    queryset = Patient.objects.all().order_by("-created_at")
    serializer_class = PatientSerializer
    parser_classes = [MultiPartParser, FormParser, JSONParser]
    permission_classes = [PublicReadCreatePermission]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if not serializer.is_valid():
            return Response({"errors": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
        patient = serializer.save()
        return Response(self.get_serializer(patient).data, status=status.HTTP_201_CREATED)


class AttachmentViewSet(viewsets.ModelViewSet):
    queryset = Attachment.objects.select_related("patient").order_by("-created_at")
    serializer_class = AttachmentSerializer
    parser_classes = [MultiPartParser, FormParser, JSONParser]
    permission_classes = [PublicReadCreatePermission]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if not serializer.is_valid():
            return Response({"errors": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
        obj = serializer.save()
        return Response(self.get_serializer(obj).data, status=status.HTTP_201_CREATED)


# ---- Health & Storage diag ----
from django.views.decorators.csrf import csrf_exempt
from django.core.files.base import ContentFile
from django.core.files.storage import default_storage
import traceback

@csrf_exempt
def health(request):
    return JsonResponse({"status": "ok"})

@csrf_exempt
def storage_diag(request):
    """
    Prueba escritura/lectura en DEFAULT_FILE_STORAGE.
    Si falla, attachments no van a poder guardarse.
    """
    try:
        name = "diag/diagnostico.txt"
        default_storage.save(name, ContentFile(b"ok"))
        url = default_storage.url(name)
        default_storage.delete(name)
        return JsonResponse({"ok": True, "example_url": url})
    except Exception as e:
        return JsonResponse(
            {"ok": False, "error": str(e), "traceback": traceback.format_exc()},
            status=500
        )
