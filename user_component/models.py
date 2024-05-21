from django.db import models
from django.contrib.auth.models import User
from admin_component.models import App


class Screenshot(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    app = models.ForeignKey(App, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='screenshots/')
    uploaded_at = models.DateTimeField(auto_now_add=True)
    
