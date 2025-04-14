from django.db import models

from orders.models import Order

class Shipment(models.Model):
    order = models.OneToOneField(Order, on_delete=models.CASCADE)
    tracking_number = models.CharField(max_length=100, unique=True)
    carrier = models.CharField(max_length=100)
    status = models.CharField(
        max_length=20,
        choices=[('In Transit', 'In Transit'), ('Delivered', 'Delivered'), ('Returned', 'Returned')],
        default='In Transit'
    )
    estimated_delivery = models.DateField()
    shipped_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Shipment {self.tracking_number} - {self.status}"
