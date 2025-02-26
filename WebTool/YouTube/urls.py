from django.contrib import admin
from django.urls import path
from .views import YouTubeDownloaderView

app_name = 'YouTube'

urlpatterns = [
    path('admin/', admin.site.urls),
    path('youtube', YouTubeDownloaderView.as_view(), name='youtube'),
]