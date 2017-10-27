from django.contrib import admin

# Register your models here.

from .models import User, Server, Role, PublicKey

class PublicKeyInline(admin.TabularInline):
    model = PublicKey
    extra = 3

class UserAdmin(admin.ModelAdmin):
    inlines = [PublicKeyInline]
    list_display = ('name', 'uid', 'gecos', 'disabled')
    search_fields = ['name']

admin.site.register(User, UserAdmin)
admin.site.register(Server)
admin.site.register(Role)
