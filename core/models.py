from django.db import models

# Create your models here.


class BilibiliURI(models.Model):
    url = models.CharField(max_length=200)


class BulletScreen(models.Model):
    URI_ID = models.ForeignKey(BilibiliURI, on_delete=models.CASCADE)
    date = models.CharField(max_length=30)
    content = models.CharField(max_length=200)
