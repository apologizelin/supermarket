from django.db import models


# Create your models here.
class Users(models.Model):
    class Users(models.Model):
        username = models.CharField(max_length=50)
        pwd = models.CharField(max_length=50)

        class Meta:
            db_table = "users"

        def __str__(self):
            return self.username
