from django.contrib import admin

from .models import BoastUser


class AdminBoastUser(admin.ModelAdmin):
    list_display = ('username', 'is_activated',)


admin.site.register(BoastUser, AdminBoastUser)
