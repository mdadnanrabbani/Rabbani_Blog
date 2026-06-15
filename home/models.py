from django.contrib.auth.models import User
from django.db import models



# Create your models here.


class Category(models.Model):
    category_name = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, default='cat')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    def __str__(self):
        return self.category_name


class BlogPost(models.Model):
    STATUS_CHOICES = {
        'published' : 'Published',
        'draft' : 'Draft',
    }
    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200)
    short_description = models.TextField()
    content = models.TextField()
    featured_img = models.ImageField(upload_to='images/%Y/%m')
    status = models.CharField(choices=STATUS_CHOICES)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    is_featured = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title


class Contact(models.Model):
    name = models.CharField(max_length=200)
    email = models.EmailField()
    subject = models.CharField(max_length=200)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    def __str__(self):
        return self.name


class Comments(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    blog_post = models.ForeignKey(BlogPost, on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    def __str__(self):
        return self.content