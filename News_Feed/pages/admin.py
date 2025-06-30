from django.contrib import admin
from .models import NewsPost,Like, Comment, SavedPost
# Register your models here.

@admin.register(NewsPost)
class NewsPostAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'author', 'created_at', 'is_published')
    list_filter = ('category', 'is_published', 'created_at')
    search_fields = ('title', 'content')
    prepopulated_fields = {'slug': ('title',)}
    ordering = ('-created_at',)

admin.site.register(Like)
admin.site.register(Comment)
admin.site.register(SavedPost)




 
