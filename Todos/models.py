from django.db import models
from Todo import settings
# Create your models here.
class Todos(models.Model):

    user = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE)
    title = models.CharField(max_length=50)
    infos = models.TextField(max_length = 200)
    def __str__(self):
        return self.title 