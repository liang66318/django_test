from django.db import models

# Create your models here.
from django.db import models
from django.utils import timezone

class Post(models.Model):
    created_time = models.TextField(default="")
    title = models.TextField(default="")
    text = models.TextField(default="")
    detailed = models.TextField(default="")
    picture = models.TextField(default="")
    big = models.IntegerField( default=0 )


    class Meta:
        db_table = "news"

    def publish(self):
        self.save()

    def __str__(self):
        return self.title