from django.db import models

class Cinema(models.Model):
    name = models.CharField(max_length=255, verbose_name="Cinema Name")
    address = models.TextField(verbose_name="Address")
    phone_number = models.CharField(max_length=20, blank=True, null=True, verbose_name="Phone Number")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Cinema"
        verbose_name_plural = "Cinemas"

