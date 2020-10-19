from django.db import models


class Request(models.Model):
    url = models.TextField()
    date = models.DateTimeField(auto_now_add=True)
    uuid = models.TextField(null=True)
