from django.db import models

class Status(models.Model):
    key = models.IntegerField()
    name = models.CharField(max_length=25)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "Statuses"


class Product(models.Model):
    name = models.CharField(max_length=255)
    status = models.ForeignKey(Status, on_delete=models.CASCADE, related_name='statuses')
    stock = models.IntegerField()
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

