from django.contrib import admin
from passlib.hash import sha512_crypt
from sshpubkeys import SSHKey

# Register your models here.

from .models import User, Server, Role, PublicKey

class PublicKeyInline(admin.TabularInline):
    model = PublicKey
    extra = 1
    def save_model(self, request, obj, form, change):
        ssh = SSHKey(request.POST['key'])
        ssh.parse()
        obj.finger_print = ssh.hash_md5()
        super(PublicKeyInline, self).save_model(request, obj, form, change)

class UserAdmin(admin.ModelAdmin):
    inlines = [PublicKeyInline]
    list_display = ('name', 'uid', 'gecos', 'disabled')
    search_fields = ['name']
    def save_model(self, request, obj, form, change):
        if not request.POST['password'].startswith('$6$'):
            obj.password = sha512_crypt.using(rounds=5000).hash(request.POST['password'])
        super(UserAdmin, self).save_model(request, obj, form, change)

admin.site.register(User, UserAdmin)
admin.site.register(Server)
admin.site.register(Role)
