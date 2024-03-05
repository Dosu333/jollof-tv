from django.db import models
from django.contrib.auth import get_user_model
import uuid

class VideoFile(models.Model):
    id = models.UUIDField(primary_key=True, editable=False, default=uuid.uuid4)
    owner = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, blank=True, null=True)
    title = models.CharField(max_length=255, blank=True, null=True)
    video_file = models.FileField(upload_to='video_files')

    def __str__(self):
        return self.title