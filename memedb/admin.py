from django.contrib import admin

from .models import Meme


class MemeAdmin(admin.ModelAdmin):
    list_display = ["uuid", "owner", "created_at"]
    list_select_related = ["owner"]


admin.site.register(Meme, MemeAdmin)
