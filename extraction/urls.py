from django.urls import path
from .views import extract_and_upload_to_mongodb


urlpatterns = [
    path('', extract_and_upload_to_mongodb,
         name='extract_and_upload_to_mongodb'),
]
