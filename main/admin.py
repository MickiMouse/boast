from django.contrib import admin

from .models import BoastPost, Comment


class AdminBoastPost(admin.ModelAdmin):
    list_display = ('author', 'created_at', 'like_count')

    def like_count(self, obj):
        return obj.likes.count()


admin.site.register(BoastPost, AdminBoastPost)
