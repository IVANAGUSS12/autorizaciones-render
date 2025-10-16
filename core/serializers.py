from rest_framework import serializers
from .models import Patient, Attachment

class AttachmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Attachment
        fields = ["id", "patient", "kind", "file", "name", "created_at", "url"]

class PatientSerializer(serializers.ModelSerializer):
    attachments = AttachmentSerializer(many=True, read_only=True)

    class Meta:
        model = Patient
        fields = "__all__"
