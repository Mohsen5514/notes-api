from django.db import models
from django.contrib.auth.models import User


# Create your models here.
class Task(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="tasks",null=True)
    title=models.CharField(max_length=200)
    description=models.TextField(blank=True,null=True)
    completed=models.BooleanField(default=False)
    created_at=models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
    

class Note(models.Model):
    title=models.CharField(max_length=200)
    content=models.TextField(blank=True,null=True)
    created_at=models.DateTimeField(auto_now_add=True)
    user=models.ForeignKey(User,on_delete=models.CASCADE, related_name="notes")