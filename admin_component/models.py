from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

class Category(models.Model):
    name = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return self.name

class SubCategory(models.Model):
    name = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return self.name

class App(models.Model):
    app_name = models.CharField(max_length=255)
    app_link = models.URLField()
    app_category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True)
    sub_category = models.ForeignKey(SubCategory, on_delete=models.SET_NULL, null=True, blank=True)
    points = models.IntegerField()
    app_image = models.ImageField(upload_to='app_images/')

    def __str__(self):
        return self.app_name
    
class AppUsers(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    app = models.ForeignKey(App, on_delete=models.CASCADE)
    date_downloaded = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"{self.user.username} - {self.app.name}"
    
