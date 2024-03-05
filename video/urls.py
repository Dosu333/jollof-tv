from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import VideoFileViewSet

router = DefaultRouter()

router.register('videos', VideoFileViewSet)

urlpatterns = [
    path('', include(router.urls)),
]