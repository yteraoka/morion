from django.db import models

# Create your models here.

class Role(models.Model):
    name = models.CharField(max_length=256)
    description = models.CharField(max_length=256, blank=True)

    def __str__(self):
        return self.name


class User(models.Model):
    name = models.CharField(max_length=32)
    uid = models.IntegerField()
    gecos = models.CharField(max_length=128, blank=True)
    shell = models.CharField(max_length=32, blank=True)
    password = models.CharField(max_length=256, null=True, blank=True)
    directory = models.CharField(max_length=256, blank=True)
    expiry_date = models.DateField(null=True, blank=True)
    disabled = models.BooleanField()
    roles = models.ManyToManyField(Role, through='UserRoleMembership')

    def __str__(self):
        return self.name


class PublicKey(models.Model):
    name = models.CharField(max_length=256)
    key = models.TextField()
    finger_print = models.CharField(max_length=256, blank=True, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.key


class Server(models.Model):
    name = models.CharField(max_length=256)
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


class ServerRoleMembership(models.Model):
    server = models.ForeignKey(Server, on_delete=models.CASCADE)
    role = models.ForeignKey(Role, on_delete=models.CASCADE)
    joined_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return "{0}--{1}".format(self.server.name, self.role.name)
