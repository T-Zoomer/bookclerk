import uuid
from django.db import models
from django.utils import timezone


class RecommendationRequest(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user_preferences = models.TextField(help_text="User's book preferences and interests")
    created_at = models.DateTimeField(default=timezone.now)
    
    def __str__(self):
        return f"Request at {self.created_at.strftime('%Y-%m-%d %H:%M')}"


class BookRecommendation(models.Model):
    request = models.ForeignKey(RecommendationRequest, on_delete=models.CASCADE, related_name='recommendations')
    title = models.CharField(max_length=200)
    author = models.CharField(max_length=200)
    description = models.TextField()
    reason = models.TextField(help_text="Why this book was recommended")
    amazon_url = models.URLField(blank=True, null=True, help_text="Amazon affiliate link")
    created_at = models.DateTimeField(default=timezone.now)
    
    def __str__(self):
        return f"{self.title} by {self.author}"
