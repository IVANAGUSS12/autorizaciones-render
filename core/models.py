from django.db import models

SECTOR_CHOICES = (
    ("trauma", "Traumatología"),
    ("hemo", "Hemodinamia"),
)

ESTADO_CHOICES = (
    ("Pendiente","Pendiente"),
    ("Solicitado","Solicitado"),
    ("Rechazado por cobertura","Rechazado por cobertura"),
    ("Autorizado","Autorizado"),
    ("Autorizado material pendiente","Autorizado material pendiente"),
)

class Patient(models.Model):
    nombre = models.CharField(max_length=200)
    dni = models.CharField(max_length=32)
    email = models.EmailField()
    telefono = models.CharField(max_length=64)
    cobertura = models.CharField(max_length=160)
    medico = models.CharField(max_length=160)
    observaciones = models.TextField(blank=True)
    fecha_cx = models.DateField(null=True, blank=True)
    sector_code = models.CharField(max_length=10, choices=SECTOR_CHOICES, default="trauma")
    estado = models.CharField(max_length=40, choices=ESTADO_CHOICES, default="Pendiente")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.nombre} ({self.dni})"


def attachment_path(instance, filename):
    return f"adjuntos/{instance.created_at:%Y/%m/%d}/{filename}"

class Attachment(models.Model):
    KIND_CHOICES = (
        ("orden","orden"),
        ("dni","dni"),
        ("credencial","credencial"),
        ("materiales","materiales"),
        ("otro","otro"),
    )
    patient = models.ForeignKey(Patient, related_name="attachments", on_delete=models.CASCADE)
    kind = models.CharField(max_length=20, choices=KIND_CHOICES, default="otro")
    file = models.FileField(upload_to=attachment_path)
    name = models.CharField(max_length=200, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    @property
    def url(self):
        try:
            return self.file.url
        except Exception:
            return ""
