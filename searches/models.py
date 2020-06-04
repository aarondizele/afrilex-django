from django.conf import settings
from django.db import models

# Create your models here.
class SearchQuery(models.Model):
    user           = models.ForeignKey(settings.AUTH_USER_MODEL, blank=True, null=True, on_delete=models.SET_NULL)
    query          = models.CharField(max_length=200)
    place          = models.CharField(max_length=200)
    timestamp      = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.query