from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from .models import VideoFile
from .serializers import VideoFileSerializer


class VideoFileViewSet(viewsets.ModelViewSet):
    queryset = VideoFile.objects.all()
    serializer_class = VideoFileSerializer
    http_method_names = ['get',]
    permission_classes = [IsAuthenticated, ]