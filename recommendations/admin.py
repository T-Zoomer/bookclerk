from django.contrib import admin
from .models import RecommendationRequest, BookRecommendation


class BookRecommendationInline(admin.TabularInline):
    model = BookRecommendation
    extra = 0
    readonly_fields = ['created_at']
    fields = ['title', 'author', 'description', 'reason', 'amazon_url', 'created_at']


@admin.register(RecommendationRequest)
class RecommendationRequestAdmin(admin.ModelAdmin):
    list_display = ['id', 'created_at', 'truncated_preferences', 'recommendation_count']
    list_filter = ['created_at']
    search_fields = ['user_preferences']
    readonly_fields = ['created_at']
    ordering = ['-created_at']
    inlines = [BookRecommendationInline]
    
    def truncated_preferences(self, obj):
        return obj.user_preferences[:50] + '...' if len(obj.user_preferences) > 50 else obj.user_preferences
    truncated_preferences.short_description = 'User Preferences'
    
    def recommendation_count(self, obj):
        return obj.recommendations.count()
    recommendation_count.short_description = 'Books Recommended'


@admin.register(BookRecommendation)
class BookRecommendationAdmin(admin.ModelAdmin):
    list_display = ['title', 'author', 'request', 'created_at']
    list_filter = ['created_at', 'request']
    search_fields = ['title', 'author', 'description']
    readonly_fields = ['created_at']
    ordering = ['-created_at']
