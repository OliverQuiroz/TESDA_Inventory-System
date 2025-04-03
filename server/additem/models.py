from django.db import models
import qrcode  # type: ignore
from io import BytesIO
from django.core.files.base import ContentFile
from django.utils import timezone

class Item(models.Model):
    inventory_number = models.CharField(max_length=100, unique=True)
    product_name = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    date_of_purchase = models.DateField(blank=True, null=True)
    recipient = models.CharField(max_length=255, blank=True)
    recipient_history = models.JSONField(default=list, blank=True)  # For PostgreSQL

    CLASSIFICATION_CHOICES = [
        ("SE", "Semi-Expendable"),
        ("PPE", "Property, Plant & Equipment"),
    ]
    classification = models.CharField(
        max_length=10,
        choices=CLASSIFICATION_CHOICES,
        default="SE"
    )

    qr_code = models.ImageField(upload_to="qr_codes/", blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def generate_qr_code(self):
        qr_data = (
            f"Inventory No: {self.inventory_number}\n"
            f"Product: {self.product_name}\n"
            f"Description: {self.description}\n"
            f"Price: {self.price}\n"
            f"Date of Purchase: {self.date_of_purchase}\n"
            f"Recipient: {self.recipient}\n"
            f"Classification: {self.classification}"
        )

        qr = qrcode.make(qr_data)
        buffer = BytesIO()
        qr.save(buffer, format="PNG")

        filename = f"{self.inventory_number}_qr.png"
        self.qr_code.save(filename, ContentFile(buffer.getvalue()), save=False)

    def save(self, *args, **kwargs):
        # Detect recipient change
        if self.pk:
            old = Item.objects.get(pk=self.pk)
            if old.recipient != self.recipient:
                self._add_to_recipient_history()
        elif not self.recipient_history:
            self._add_to_recipient_history()

        # Generate QR code if missing
        if not self.qr_code:
            self.generate_qr_code()

        super().save(*args, **kwargs)

    def _add_to_recipient_history(self):
        today = timezone.now().date().isoformat()
        new_entry = {
            "name": self.recipient,
            "date": today
        }

        # Avoid duplicate history entries
        if new_entry not in self.recipient_history:
            self.recipient_history.append(new_entry)

    def __str__(self):
        return f"{self.inventory_number} - {self.product_name}"
