from django.db import models
from django.utils import timezone
from  account.models import Account
import os
from django.conf import settings
class Category(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name
    
class Post(models.Model):
    company_name = models.CharField(max_length=200)
    decription = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    author=models.ForeignKey(Account, on_delete=models.CASCADE)
    image=models.ImageField(upload_to='posts')
    location=models.CharField(max_length=100)
    deadline=models.DateTimeField()
    vacancy=models.TextField(blank=True, null=True)
    attributes=models.TextField(blank=True, null=True)
    price_range=models.CharField(max_length=10, blank=True, null=True)
    url=models.URLField(max_length=255, blank=True, null=True)
    expired = models.BooleanField(default=False)
    
    def save(self, *args, **kwargs):
        # Check if the post's deadline has passed
        if self.deadline < timezone.now():
            self.expired = True

        super().save(*args, **kwargs)

        # Delete the image file if expired is True
        if self.expired:
            if self.image:
                # Construct the full path to the image file
                image_path = os.path.join(settings.MEDIA_ROOT, str(self.image))
                
                # Check if the file exists and delete it
                if os.path.exists(image_path):
                    os.remove(image_path)
                    # You can also delete the corresponding database entry for the image if needed
                    self.image.delete(save=False)

    def __str__(self):
        return self.company_name
