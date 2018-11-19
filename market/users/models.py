from django.db import models


# Create your models here.
class Users(models.Model):
    username = models.CharField(max_length=50)
    password = models.CharField(max_length=50)
    time = models.DateField(auto_now_add=True)

    class Meta:
        db_table = "users"

    def __str__(self):
        return self.username

