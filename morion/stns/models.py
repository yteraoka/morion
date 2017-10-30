from django.db import models

# Create your models here.

class User(models.Model):
    name = models.CharField(max_length=32)
    uid = models.IntegerField()
    gecos = models.CharField(max_length=128, blank=True)
    shell = models.CharField(max_length=32, blank=True)
    password = models.CharField(max_length=256, null=True, blank=True)
    directory = models.CharField(max_length=256, blank=True)
    expiry_date = models.DateField(null=True, blank=True)
    disabled = models.BooleanField()

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

    def __str__(self):
        return self.name

class Role(models.Model):
    name = models.CharField(max_length=256)
    user = models.ManyToManyField(User)
    server = models.ManyToManyField(Server)
    description = models.CharField(max_length=256, blank=True)

    def __str__(self):
        return self.name
