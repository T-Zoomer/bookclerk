from django.contrib import admin
from .models import RecommendationRequest, BookRecommendation


@admin.register(RecommendationRequest)
class RecommendationRequestAdmin(admin.ModelAdmin):
    list_display = ['id', 'created_at', 'truncated_preferences']
    list_filter = ['created_at']
    search_fields = ['user_preferences']
    readonly_fields = ['created_at']
    ordering = ['-created_at']
    
    def truncated_preferences(self, obj):
        return obj.user_preferences[:50] + '...' if len(obj.user_preferences) > 50 else obj.user_preferences
    truncated_preferences.short_description = 'User Preferences'


@admin.register(BookRecommendation)
class BookRecommendationAdmin(admin.ModelAdmin):
    list_display = ['title', 'author', 'request', 'created_at']
    list_filter = ['created_at', 'request']
    search_fields = ['title', 'author', 'description']
    readonly_fields = ['created_at']
    ordering = ['-created_at']
