from django.db import models
from django.contrib.auth.models import User

class Blocktable(models.Model):
    title = models.CharField(max_length=100)
    content = models.CharField(max_length=1000)
    authId = models.ForeignKey(User,on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now_add=True, blank=True)
    isPrivate = models.IntegerField(default=0)

class CommentTable(models.Model):
    content = models.CharField(max_length=1000)
    date = models.DateTimeField(auto_now_add=True, blank=True)
    blockId = models.ForeignKey(Blocktable,on_delete=models.CASCADE)
    authId = models.ForeignKey(User,on_delete=models.CASCADE)
