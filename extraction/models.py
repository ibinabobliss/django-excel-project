# models.py
from django.db import models


class ExcelData(models.Model):
    name = models.CharField(max_length=255)
    value = models.FloatField()

    def __str__(self):
        return f"{self.name} - {self.value}"
