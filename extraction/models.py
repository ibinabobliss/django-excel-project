# your_app_name/models.py
from django.db import models


class ExtractedData(models.Model):
    First_Name = models.CharField(max_length=150)
    Last_Name = models.CharField(max_length=225)
    Degree = models.CharField(max_length=255)
    Relationship = models.CharField(max_length=255)
    Skin_Color = models.CharField(max_length=255)

    def __str__(self):
        return f"{self.First_Name} {self.Last_Name}"
