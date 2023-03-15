from django.db import models
from users.models import User
from django.core.validators import MaxValueValidator, MinValueValidator


class Title(models.Model):
    pass


class Review(models.Model):
    
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='reviews')
    text = models.TextField()
    pub_date = models.DateTimeField('Дата публикации', auto_now_add=True)
    title = models.ForeignKey(
        Title,
        on_delete=models.CASCADE,
        related_name="reviews",
    )
    rate = models.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(10)]
    )
    
    class Meta:
        ordering = ['-pub_date']
        constraints = [
            models.UniqueConstraint(fields=['author', 'title'],
                                    name='unique_reviews')
        ]

    def __str__(self):
        return self.author
    
    
class Comment(models.Model):
    
    review = models.ForeignKey(
        Review, on_delete=models.CASCADE, related_name='comments')
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='comments')
    text = models.TextField()
    pub_date = models.DateTimeField('Дата публикации', auto_now_add=True)
    
    class Meta:
        ordering = ['-pub_date']

    def __str__(self):
        return self.text