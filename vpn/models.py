from django.db import models
from django.contrib.auth.models import User


class Site(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    url = models.TextField('url', primary_key=True)
    name = models.CharField('name', max_length=255)

    def __str__(self):
        return self.name



class SiteStats(models.Model):
    site = models.ForeignKey(Site, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    from_path = models.TextField()
    to_path = models.TextField()
    data_sent = models.IntegerField(default=0)
    data_received = models.IntegerField(default=0)
