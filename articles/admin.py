from django.contrib import admin

# Register your models here.
from  .models import  *

class CommentInLine(admin.TabularInline):
    model = Comment
    extra = 0


class ArticleAdmin(admin.ModelAdmin):
    inlines = [CommentInLine]

admin.site.register(Aricles,ArticleAdmin)
admin.site.register(Comment)
admin.site.register(Category)