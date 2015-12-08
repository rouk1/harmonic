from django.db import models


class Section(models.Model):
    title = models.CharField(max_length=128)
