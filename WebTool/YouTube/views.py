from django.shortcuts import render, HttpResponse
from django.conf import settings
from .forms import YouTubeForm
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
import yt_dlp
import os

class YouTubeDownloaderView(LoginRequiredMixin, View):  # Add LoginRequiredMixin
    template_name = 'YouTube/ytdownload.html'

    def get(self, request, *args, **kwargs):
        # Render the form for GET requests
        form = YouTubeForm()
        return render(request, self.template_name, {'form': form})

    def post(self, request, *args, **kwargs):
        # Handle form submission for POST requests
        form = YouTubeForm(request.POST)
        if form.is_valid():
            url = form.cleaned_data['url']

            try:
                # Create a temporary directory if it doesn't exist
                temp_dir = os.path.join(settings.BASE_DIR, 'temp_downloads')
                os.makedirs(temp_dir, exist_ok=True)

                # Set download options to prioritize the highest quality
                ydl_opts = {
                    'format': 'bestvideo[height<=2160]+bestaudio/best[height<=2160]',  # Prioritize up to 4K (2160p)
                    'outtmpl': os.path.join(temp_dir, '%(title)s.%(ext)s'),  # Save to the temporary directory
                }

                # Download the video
                with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                    info_dict = ydl.extract_info(url, download=True)
                    video_title = info_dict.get('title', 'video')
                    video_ext = info_dict.get('ext', 'mp4')
                    video_filename = f"{video_title}.{video_ext}"
                    video_path = os.path.join(temp_dir, video_filename)

                # Serve the file to the user
                with open(video_path, 'rb') as video_file:
                    response = HttpResponse(video_file.read(), content_type='video/mp4')
                    response['Content-Disposition'] = f'attachment; filename="{video_filename}"'

                # Delete the file from the server after serving it
                os.remove(video_path)

                return response

            except Exception as e:
                return HttpResponse(f"An error occurred: {e}")
        else:
            # If the form is invalid, re-render the form with errors
            return render(request, self.template_name, {'form': form})

# # defining function
# def youtube(request):
#     if request.method == 'POST':
#         form = YouTubeForm(request.POST)
#         if form.is_valid():
#             url = form.cleaned_data['url']
#
#             try:
#                 # Create a temporary directory if it doesn't exist
#                 temp_dir = os.path.join(settings.BASE_DIR, 'temp_downloads')
#                 os.makedirs(temp_dir, exist_ok=True)
#
#                 # Set download options
#                 ydl_opts = {
#                     # 'format': 'best',  # Download the best quality available
#                     'format': 'bestvideo[height<=2160]+bestaudio/best[height<=2160]',  # Download the best quality available
#                     'outtmpl': os.path.join(temp_dir, '%(title)s.%(ext)s'),  # Save to the temporary directory
#                 }
#
#                 # Download the video
#                 with yt_dlp.YoutubeDL(ydl_opts) as ydl:
#                     info_dict = ydl.extract_info(url, download=True)
#                     video_title = info_dict.get('title', 'video')
#                     video_ext = info_dict.get('ext', 'mp4')
#                     video_filename = f"{video_title}.{video_ext}"
#                     video_path = os.path.join(temp_dir, video_filename)
#
#                 # Serve the file to the user
#                 with open(video_path, 'rb') as video_file:
#                     response = HttpResponse(video_file.read(), content_type='video/mp4')
#                     response['Content-Disposition'] = f'attachment; filename="{video_filename}"'
#
#                 # Delete the file from the server after serving it
#                 try:
#                     os.remove(video_path)
#                 except Exception as e:
#                     print(f"Failed to delete file: {e}")
#
#                 return response
#
#             except Exception as e:
#                 return HttpResponse(f"An error occurred: {e}")
#     else:
#         form = YouTubeForm()
#     return render(request, 'YouTube/ytdownload.html', {'form': form})