from django.contrib import admin
from django.utils.html import format_html
from .models import Profile, Photo, Status


class ProfileAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'admin_img', 'phone', 'address_1',
                    'city', 'state', 'zipcode', 'temper', 'available', )
    search_fields = ('first_name__icontains', 'last_name__icontains')

    def admin_img(self, obj) -> str:
        return format_html(f'<img src="/media/{obj.img}" width="35" height="35" />')


admin.site.register(Profile, ProfileAdmin)
admin.site.register(Photo)
admin.site.register(Status)
