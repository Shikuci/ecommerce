from django.conf import settings
from django.db import models


class Account(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="account")
    phone_number = models.CharField(max_length=20)
    pro_image = models.ImageField(upload_to="photos/accounts", blank=True)

    def __str__(self):
        return self.user.email or self.user.get_username()
