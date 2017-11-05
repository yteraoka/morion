from django.contrib import admin
from passlib.hash import sha512_crypt
from sshpubkeys import SSHKey

# Register your models here.

from .models import Group, User, Server, Role, PublicKey, UserRoleMembership, ServerRoleMembership

class UserRoleInline(admin.StackedInline):
    model = UserRoleMembership
    extra = 1

class ServerRoleInline(admin.StackedInline):
    model = ServerRoleMembership
    extra = 1

class PublicKeyInline(admin.TabularInline):
    model = PublicKey
    extra = 1
    def save_model(self, request, obj, form, change):
        ssh = SSHKey(request.POST['key'])
        ssh.parse()
        obj.finger_print = ssh.hash_md5()
        super(PublicKeyInline, self).save_model(request, obj, form, change)

class UserAdmin(admin.ModelAdmin):
    inlines = [PublicKeyInline, UserRoleInline]
    list_display = ('name', 'uid', 'gecos', 'disabled')
    search_fields = ['name']
    def save_model(self, request, obj, form, change):
        obj.name = obj.name.lower()
        if request.POST['shell'] == '':
            obj.shell = '/bin/bash'
        if request.POST['directory'] == '':
            obj.directory = '/home/' + obj.name
        if request.POST['password'] == '':
            obj.password = None
        elif not request.POST['password'].startswith('$6$'):
            obj.password = sha512_crypt.using(rounds=5000).hash(request.POST['password'])
        super(UserAdmin, self).save_model(request, obj, form, change)

class ServerAdmin(admin.ModelAdmin):
    inlines = [ServerRoleInline]
    def save_model(self, request, obj, form, change):
        if request.POST['password'] == '':
            obj.password = None
        elif not request.POST['password'].startswith('$6$'):
            obj.password = sha512_crypt.using(rounds=5000).hash(request.POST['password'])
        super(ServerAdmin, self).save_model(request, obj, form, change)

admin.site.register(User, UserAdmin)
admin.site.register(Server, ServerAdmin)
admin.site.register(Role)
admin.site.register(Group)
