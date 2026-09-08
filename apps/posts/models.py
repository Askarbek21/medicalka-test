from django.core.validators import MinLengthValidator
from django.db import models

from apps.core.models import BaseModel 
from apps.auth.models import User


class Post(BaseModel):
    title = models.CharField(
        max_length=255,
        validators=[MinLengthValidator(5)]
    )

    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='posts')
    content = models.TextField(max_length=10000)

    def __str__(self):
        return self.title
    
    class Meta:
        ordering = ['-created_at']


class Comment(BaseModel):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='comments')
    content = models.TextField(max_length=2000)

    def __str__(self):
        return f'Коммент {self.author.username} на {self.post.title}'

    class Meta:
        ordering = ['-created_at']
        

class Like(BaseModel):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='likes')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='likes')

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['post', 'user'],
                name='unique_post_like',
            )
        ]

    def __str__(self):
        return f'Лайк {self.user.username} на {self.post.title}'