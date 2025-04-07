from django.contrib import admin
from .models import (
    CustomUser,
    Question,
    Answer,
    Comment,
    QuestionLike,
    AnswerLike
)

from django.contrib.auth.admin import UserAdmin

admin.site.register(CustomUser, UserAdmin)

@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ['id', 'title', 'author', 'created_at']
    search_fields = ['title', 'description', 'author__username']

@admin.register(Answer)
class AnswerAdmin(admin.ModelAdmin):
    list_display = ['id', 'question', 'author', 'created_at']
    search_fields = ['content', 'author__username', 'question__title']

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ['id', 'answer', 'author', 'created_at']
    search_fields = ['text', 'author__username', 'answer__question__title']

@admin.register(QuestionLike)
class QuestionLikeAdmin(admin.ModelAdmin):
    list_display = ['id', 'question', 'user', 'liked_at']
    search_fields = ['user__username', 'question__title']

@admin.register(AnswerLike)
class AnswerLikeAdmin(admin.ModelAdmin):
    list_display = ['id', 'answer', 'user', 'liked_at']
    search_fields = ['user__username', 'answer__question__title']
