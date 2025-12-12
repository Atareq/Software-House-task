from django.db import models
from safedelete.models import SafeDeleteModel


class Customer(SafeDeleteModel):
    customer_code = models.CharField(max_length=50, unique=True)
    name = models.CharField(max_length=200)

    phone = models.CharField(max_length=20)
    address = models.TextField()
    email = models.EmailField()

    opening_balance = models.DecimalField(
        max_digits=10, decimal_places=2, default=0.00
    )

    def __str__(self):
        return f"{self.name} - {self.customer_code}"
