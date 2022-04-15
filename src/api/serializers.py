from rest_framework import serializers

from .models import GeneratorTask


class GeneratorTaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = GeneratorTask
        fields = [
            "id",
            "created_at",
            "project_id",
            "data",
            "file_format",
            "output_file",
            "status",
            "error",
        ]

        extra_kwargs = {
            "id": {"read_only": True},
            "created_at": {"read_only", True},
            "output_file": {"read_only": True},
            "status": {"read_only": True},
            "error": {"read_only": True},
        }
