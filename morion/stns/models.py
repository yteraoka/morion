from django.db import models

# Create your models here.

class Role(models.Model):
    name = models.CharField(max_length=256, unique=True)
    description = models.CharField(max_length=256, blank=True)

    def __str__(self):
        return self.name


class Group(models.Model):
    name = models.CharField(max_length=32, unique=True)
    gid = models.IntegerField(unique=True)
    description = models.CharField(max_length=256, blank=True)

    def __str__(self):
        return "{0} (gid:{1})".format(self.name, self.gid)


class User(models.Model):
    name = models.CharField(max_length=32, unique=True)
    uid = models.IntegerField(unique=True)
    gecos = models.CharField(max_length=128, blank=True)
    shell = models.CharField(max_length=32, blank=True)
    password = models.CharField(max_length=256, null=True, blank=True)
    directory = models.CharField(max_length=256, blank=True)
    expiry_date = models.DateField(null=True, blank=True)
    disabled = models.BooleanField()
    groups = models.ManyToManyField(Group, through='UserGroupMembership')
    roles = models.ManyToManyField(Role, through='UserRoleMembership')

    def __str__(self):
        return self.name


class PublicKey(models.Model):
    name = models.CharField(max_length=256)
    key = models.TextField()
    finger_print = models.CharField(max_length=256, blank=True, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='publickeys')

    def __str__(self):
        return self.key


class Server(models.Model):
    name = models.CharField(max_length=256, unique=True)
    password = models.CharField(max_length=256, blank=True, null=True)
    description = models.CharField(max_length=256, blank=True)
    roles = models.ManyToManyField(Role, through='ServerRoleMembership')

    def __str__(self):
        return self.name


class UserRoleMembership(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    role = models.ForeignKey(Role, on_delete=models.CASCADE)
    joined_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return "{0}--{1}".format(self.user.name, self.role.name)


class UserGroupMembership(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    group = models.ForeignKey(Group, on_delete=models.CASCADE)
    primary = models.BooleanField()
    joined_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return "{0}--{1}".format(self.user.name, self.group.name)


class ServerRoleMembership(models.Model):
    server = models.ForeignKey(Server, on_delete=models.CASCADE)
    role = models.ForeignKey(Role, on_delete=models.CASCADE)
    joined_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return "{0}--{1}".format(self.server.name, self.role.name)
