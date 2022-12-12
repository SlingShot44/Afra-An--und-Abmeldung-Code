from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator
from .validators import HouseValidator
from .json_tools import houses_config
# Create your models here.

class Account(models.Model):
    uid = models.IntegerField(unique=True, primary_key=True)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    house = models.IntegerField(
        validators=[MaxValueValidator(houses_config()["max"]), MinValueValidator(houses_config()["min"]), HouseValidator(houses_config()["exclude"])])
    #expired = models.BooleanField(default=False)
    

    def __str__(self):
        return self.get_full_name()

    def get_full_name(self):
        return f"{self.first_name} {self.last_name}"
class Tour(models.Model):
    owner = models.ForeignKey(Account, on_delete=models.CASCADE)
    start = models.DateTimeField(auto_now_add=True)
    end = models.DateTimeField(null=True)
    target = models.IntegerField()
    back = models.BooleanField(default=False)
    mutable = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.owner.get_full_name()} - {self.target} - {self.start}"

    def save(self, *args, **kwargs):
        if self.mutable:
            return super().save(*args, **kwargs)

