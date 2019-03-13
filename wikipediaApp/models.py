from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

# Create your models here.

class Author(models.Model):
    username=models.CharField(max_length=200)
    password=models.CharField(max_length=200)
    make_user=models.ForeignKey(User,on_delete=models.CASCADE,blank=True,null=True)

    def __str__(self):
        return self.username

class Article(models.Model):
    title=models.CharField(max_length=200)
    text=models.TextField()
    date_created=models.DateTimeField(timezone.now(),blank=True,null=True)
    last_update=models.DateTimeField(timezone.now(),blank=True,null=True)
    image=models.ImageField(upload_to='Images',blank=True)
    key_to_User=models.ForeignKey(Author,on_delete=models.CASCADE,blank=True,null=True)

    def __str__(self):
        return self.title

class Related(models.Model):
    title=models.CharField(max_length=200)
    text=models.TextField()
    date_created=models.DateTimeField(timezone.now())
    last_update=models.DateTimeField(timezone.now())
    image=models.ImageField(upload_to='Images',blank=True)
    key_to_Article=models.ForeignKey(Article,on_delete=models.CASCADE,blank=True,null=True)

    def __str__(self):
        return self.title
