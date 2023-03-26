from django.db import models


class Contact(models.Model):
    name = models.CharField(max_length=225)
    phone = models.CharField(max_length=225, null=True, blank=True)
    email = models.EmailField(null=True, blank=True)
    message = models.TextField()

    def __str__(self):
        return f"{self.name}'s request"
