from typing import Iterable
from django.db import models
from django.contrib.auth import get_user_model
from cloudinary.models import CloudinaryField
import cloudinary
import uuid

class VideoFile(models.Model):
    id = models.UUIDField(primary_key=True, editable=False, default=uuid.uuid4)
    owner = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, blank=True, null=True)
    title = models.CharField(max_length=255, blank=True, null=True)
    video_file = models.FileField('video', blank=True, null=True)
    thumbnail = models.FileField('thumbnail', blank=True, null=True)
    # # def save(self, *args, **kwargs):
    # #     # Generate a transformation URL to extract the first frame as a thumbnail
    # #     if self.video_file and not self.thumbnail:
    # #         thumbnail_url = cloudinary.CloudinaryImage(self.video_file).video_thumbnail()
    # #         self.thumbnail = thumbnail_url
    # #     return super().save(*args, **kwargs)

    def __str__(self):
        return self.title