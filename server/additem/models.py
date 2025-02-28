from django.db import models
import qrcode
from io import BytesIO
from django.core.files.base import ContentFile

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
    )

    qr_code = models.ImageField(upload_to='qr_codes/', blank=True, null=True)  # New field

    def generate_qr_code(self):
        qr_data = f"Inventory No: {self.inventory_number}\nProduct: {self.product_name}\nDescription: {self.description}\nPrice: {self.price}\nDate: {self.date_of_purchase}\nRecipient: {self.recipient}\nClassification: {self.classification}"
        qr = qrcode.make(qr_data)

        buffer = BytesIO()
        qr.save(buffer, format="PNG")
        self.qr_code.save(f"{self.inventory_number}_qr.png", ContentFile(buffer.getvalue()), save=False)

    def save(self, *args, **kwargs):
        if not self.qr_code:  # Generate QR code if not already created
            self.generate_qr_code()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.inventory_number} - {self.product_name}"
