# excell/extraction/urls.py
from django.urls import path
from .views import extract_and_upload_to_mongodb

urlpatterns = [
    path('upload_excel/', extract_and_upload_to_mongodb, name='upload_excel'),
]
