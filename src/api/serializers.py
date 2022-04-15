from rest_framework.serializers import ModelSerializer

from .models import GeneratorTask


class GeneratorTaskSerializer(ModelSerializer):
    class Meta:
        model = GeneratorTask
        fields = "__all__"
        read_only_fields = ["id", "created_at", "output_file", "status", "error"]
