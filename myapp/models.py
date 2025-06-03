from django.db import models

class Photo(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    image = models.ImageField(upload_to='photos/')
    tags = models.CharField(max_length=100)
    uploaded_at = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey('auth.User', on_delete=models.CASCADE, null=True, blank=True)
    likes = models.ManyToManyField('auth.User', related_name='liked_photos', blank=True)
    
    def __str__(self):
        return self.title
    
    def total_likes(self):
        return self.likes.count()

class Comment(models.Model):
    photo = models.ForeignKey(Photo, on_delete=models.CASCADE, related_name='comments')
    user = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return f'Comment by {self.user.username} on {self.photo.title}'
    
class Profile(models.Model):
    user = models.OneToOneField('auth.User', on_delete=models.CASCADE)
    image = models.ImageField(upload_to='profile_pics/', default='default.jpg')
    full_name = models.CharField(max_length=100, blank=True)
    bio = models.TextField(blank=True)
    
    def __str__(self):
        return f'{self.user.username} Profile'
    
    def get_absolute_url(self):
        return f'/profile/{self.user.username}/'
    



