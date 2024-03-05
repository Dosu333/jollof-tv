from rest_framework import serializers
from user.serializers import ListUserSerializer
from .models import VideoFile

class VideoFileSerializer(serializers.ModelSerializer):
    class Meta:
        model = VideoFile
        fields = '__all__'

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        owner_data =  ListUserSerializer(instance.owner).data
        representation['owner'] = owner_data['first_name'] + ' ' + owner_data['last_name']
        return representation