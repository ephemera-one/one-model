import uuid

from django.db import models


class BlenderProjects(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    project_file = models.FileField()


class GeneratorTask(models.Model):
    created_at = models.DateField(auto_now=True)
    project_id = models.UUIDField()
    data = models.TextField()

    GLB = "glb"
    PNG = "png"
    FILE_FORMAT_CHOICES = [(GLB, "glb"), (PNG, "png")]

    file_format = models.CharField(
        max_length=5, choices=FILE_FORMAT_CHOICES, default=PNG
    )

    output_file = models.FileField()

    CREATED = "created"
    RUNNING = "running"
    COMPLETED = "completed"
    ERROR = "error"
    STATUS_CHOICES = [
        (CREATED, "Created"),
        (RUNNING, "Running"),
        (COMPLETED, "Completed"),
        (ERROR, "Error"),
    ]
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default=CREATED)
    error = models.TextField(default="")
