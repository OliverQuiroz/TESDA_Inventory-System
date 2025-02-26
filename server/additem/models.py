from django.db import models

class Item(models.Model):
    inventory_number = models.CharField(max_length=100)
    product_name = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    date_of_purchase = models.DateField(blank=True, null=True)
    recipient = models.CharField(max_length=255, blank=True)

    CLASSIFICATION_CHOICES = [
        ("SE", "Semi-Expendable"),
        ("PPE", "Property, Plant & Equipment"),
    ]
    
    classification = models.CharField(
        max_length=10, choices=CLASSIFICATION_CHOICES, default="SE"
    )  # Now only "SE" or "PPE" will be stored

    def __str__(self):
        return f"{self.inventory_number} - {self.product_name}"
