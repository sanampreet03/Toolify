from django.db import models

class URL(models.Model):
    original_url = models.URLField()
    short_code = models.CharField(max_length=10, unique=True)

    def __str__(self):
        return self.original_url