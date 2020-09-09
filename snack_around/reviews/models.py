from django.db import models
from django.contrib.auth import get_user_model


CHOICES = [
        (1, 1),
        (2, 2),
        (3, 3),
        (4, 4),
        (5, 5),
    ]


class Review(models.Model):
    author = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, related_name='user_reviews')
    restaurant = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, related_name='restaurant_reviews')
    score = models.IntegerField(choices=CHOICES)
    text = models.TextField(max_length=500)
    date_published = models.DateTimeField(auto_now_add=True)
