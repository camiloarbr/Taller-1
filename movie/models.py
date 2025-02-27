from django.db import models

# Create your models here.

class Movie(models.Model):
    title = models.CharField(max_length=250)  
    description = models.TextField(default="No description available")
    image = models.ImageField(upload_to='movie/images/', null=True, blank=True)
    url = models.URLField(blank=True)
    genre = models.CharField(max_length=100, default='Not specified')
    year = models.PositiveIntegerField(null=True, blank=True)

    def __str__(self):
        return self.title 