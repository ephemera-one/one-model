from typing import Dict

from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet

from .models import GeneratorTask
from .serializers import GeneratorTaskSerializer
from .tasks import generator_task


class ServiceInfoView(APIView):
    """
    View to show service info.
    """

    def get(self, request, format=None):
        """
        Return service name.
        """
        return Response({"service_name": "One Model"})


class GeneratorTaskViewSet(ModelViewSet):
    """
    API endpoint that allows generator tasks to be viewed or created.
    """

    queryset = GeneratorTask.objects.all().order_by("-created_at")
    serializer_class = GeneratorTaskSerializer

    def create(self, request):
        serializer = self.serializer_class(data=request.data)

        if serializer.is_valid():
            validated_data: Dict = serializer.validated_data

            project_id: str = validated_data["project_id"]
            data: str = validated_data["data"]
            file_format: str = validated_data["file_format"]
            callback_url: str = validated_data["callback_url"]

            task = GeneratorTask.objects.create(
                data=data,
                file_format=file_format,
                project_id=project_id,
                callback_url=callback_url,
            )

            generator_task.delay(task.id, project_id, data, file_format)

            return Response(
                {"id": task.id},
                status=status.HTTP_201_CREATED,
            )
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
