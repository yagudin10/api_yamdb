from django.contrib import admin

from .models import Comment, Review


class ReviewAdmin(admin.ModelAdmin):
    list_display = ("text", "author", "score", "pub_date", "title")


class CommentAdmin(admin.ModelAdmin):
    list_display = ("text", "author", "review", "pub_date")


admin.site.register(Review, ReviewAdmin)
admin.site.register(Comment, CommentAdmin)
