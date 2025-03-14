from django.db import models
import qrcode  # type: ignore
from io import BytesIO
from django.core.files.base import ContentFile

class Item(models.Model):
    inventory_number = models.CharField(max_length=100, unique=True)  # Prevent duplicate inventory numbers
    product_name = models.CharField(max_length=255)  # Allow duplicate product names
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

    qr_code = models.ImageField(upload_to="qr_codes/", blank=True, null=True)

    def generate_qr_code(self):
        """
        Generate a QR code containing item details and save it as an image file.
        """
        qr_data = (
            f"Inventory No: {self.inventory_number}\n"
            f"Product: {self.product_name}\n"
            f"Description: {self.description}\n"
            f"Price: {self.price}\n"
            f"Date: {self.date_of_purchase}\n"
            f"Recipient: {self.recipient}\n"
            f"Classification: {self.classification}"
        )

        qr = qrcode.make(qr_data)
        buffer = BytesIO()
        qr.save(buffer, format="PNG")

        # Save the QR code image
        filename = f"{self.inventory_number}_qr.png"
        self.qr_code.save(filename, ContentFile(buffer.getvalue()), save=False)

    def save(self, *args, **kwargs):
        """
        Override the save method to generate a QR code before saving an item.
        Only generate if we don't already have one or if you'd like to regenerate each time.
        """
        if not self.qr_code:
            self.generate_qr_code()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.inventory_number} - {self.product_name}"
