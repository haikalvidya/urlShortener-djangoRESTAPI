from django.db import models

class theURL(models.Model):
    full_url = models.TextField()
    theHash = models.TextField(unique=True)
    class Meta:
        db_table = 'url_shorten'