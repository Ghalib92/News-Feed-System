from django.db import models
from django.contrib.auth.models import User
from django.utils.text import slugify





class NewsPost(models.Model):
    title = models.CharField(max_length=255)
    slug = models.SlugField(unique=True, blank=True)
    content = models.TextField()
    image = models.ImageField(upload_to='news_images/', blank=True, null=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    
    Categories= [

            ('Politics', 'Politics'),
            ('Business', 'Business'),
            ('Technology', 'Technology'),
            ('Health', 'Health'),
            ('Science', 'Science'),
            ('Education', 'Education'),
            ('Sports', 'Sports'),
            ('Entertainment', 'Entertainment'),
            ('World', 'World'),
            ('Environment', 'Environment'),
            ('Lifestyle', 'Lifestyle'),
            ('Travel', 'Travel'),
            ('Food', 'Food'),
            ('Crime', 'Crime'),
            ('Weather', 'Weather'),
            ('Culture', 'Culture'),
            ('Opinion', 'Opinion'),
            ('Breaking', 'Breaking News'),
            ('Local', 'Local News'),
            ('Economy', 'Economy'),



            ]
    category = models.CharField(choices = Categories)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_published = models.BooleanField(default=False)
    views = models.PositiveIntegerField(default=0)

    def save(self, *args, **kwargs):
        # Automatically generate slug from title if not provided
        if not self.slug:
            self.slug = slugify(self.title)
        super(NewsPost, self).save(*args, **kwargs)

    def __str__(self):
        return self.title

