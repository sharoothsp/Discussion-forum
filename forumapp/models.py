from django.db import models
from django.conf import settings

class Mainthread(models.Model):
    name = models.TextField()
    description = models.TextField()
    number_of_views = models.IntegerField(default=0)



class Subthread(models.Model):
    name = models.TextField()
    topic = models.CharField(max_length=500)
    mainthread = models.ForeignKey(Mainthread, on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, default=1,on_delete=models.CASCADE)
    number_of_views = models.IntegerField(default=0)


class Comment(models.Model):
    reply = models.CharField(max_length=500)
    subthread = models.ForeignKey(Subthread, on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, default=1,on_delete=models.CASCADE)
