# inventory/models.py
from django.db import models
from django.core.files.base import ContentFile
from django.utils import timezone
from io import BytesIO
import qrcode


class Item(models.Model):
    # ───────── identifiers ─────────
    property_number     = models.CharField(max_length=100, unique=True)

    # ───────── basic info ──────────
    date_of_acquisition = models.DateField(blank=True, null=True)
    accountable_person  = models.CharField(max_length=255, blank=True)
    fund                = models.CharField(max_length=100, blank=True)

    article             = models.CharField(max_length=255, blank=True, default="")
    description         = models.TextField(blank=True, default="")

    # ───────── UACS ────────────────
    uacs_code           = models.CharField(max_length=50, blank=True, default="")
    UACS_CHOICES = [("SE", "Semi-Expendable"), ("PPE", "Property, Plant & Equipment")]
    uacs_category       = models.CharField(max_length=10, choices=UACS_CHOICES, default="SE", blank=True)

    # ───────── cost / qty ──────────
    unit_cost           = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    quantity            = models.PositiveIntegerField(default=1)
    total_cost          = models.DecimalField(max_digits=14, decimal_places=2, default=0)

    unit                = models.CharField(max_length=50, blank=True, default="")
    location            = models.CharField(max_length=255, blank=True, default="")

    # ───────── tracking ────────────
    accountable_history = models.JSONField(default=list, blank=True)   # NEW

    # ───────── docs ────────────────
    ics_number          = models.CharField(max_length=100, blank=True, default="")
    date_of_po          = models.DateField(blank=True, null=True)
    po_number           = models.CharField(max_length=100, blank=True, default="")
    supplier_name       = models.CharField(max_length=255, blank=True, default="")

    # ───────── QR & meta ───────────
    qr_code             = models.ImageField(upload_to="qr_codes/", blank=True, null=True)
    created_at          = models.DateTimeField(auto_now_add=True)

    # ───────────────────────────────
    def save(self, *args, **kwargs):
        # 1) auto-total
        self.total_cost = (self.unit_cost or 0) * (self.quantity or 0)

        # 2) track change of accountable_person
        if self.pk:
            old = Item.objects.get(pk=self.pk)
            if old.accountable_person != self.accountable_person:
                self._add_to_history()
        elif not self.accountable_history:
            self._add_to_history()

        # 3) generate QR if missing
        if not self.qr_code:
            self._generate_qr()

        super().save(*args, **kwargs)

    def _add_to_history(self):
        today = timezone.now().date().isoformat()
        entry = {"name": self.accountable_person, "date": today}
        if entry not in self.accountable_history:
            self.accountable_history.append(entry)

    def _generate_qr(self):
        payload = (
            f"Property No.: {self.property_number}\n"
            f"Article: {self.article}\n"
            f"Accountable: {self.accountable_person}\n"
            f"Location: {self.location}\n"
            f"Unit Cost: {self.unit_cost}\n"
            f"Qty: {self.quantity}\n"
            f"Total Cost: {self.total_cost}"
        )
        img = qrcode.make(payload)
        buffer = BytesIO()
        img.save(buffer, format="PNG")
        self.qr_code.save(f"{self.property_number}_qr.png", ContentFile(buffer.getvalue()), save=False)

    def __str__(self):
        return f"{self.property_number} – {self.article}"
