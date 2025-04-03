<template>
  <!-- Item Details Modal -->
  <div
    class="modal fade"
    id="itemModal"
    tabindex="-1"
    aria-labelledby="itemModalLabel"
    aria-hidden="true"
  >
    <div class="modal-dialog modal-dialog-centered modal-lg">
      <div class="modal-content p-4">
        <div class="modal-header border-0 text-center d-flex flex-column w-100">
          <h5 class="modal-title fw-bold text-center w-100">ITEM DETAILS</h5>
          <button
            type="button"
            class="btn-close position-absolute end-0 me-3"
            data-bs-dismiss="modal"
            aria-label="Close"
          ></button>
        </div>

        <div class="modal-body">
          <div v-for="(value, label) in itemDetails" :key="label" class="row mb-2">
            <div class="col-sm-5 fw-semibold">{{ label }}:</div>
            <div class="col-sm-7 text-break">{{ value }}</div>
          </div>

          <!-- Recipient History -->
          <div class="mb-4">
            <label class="col-sm-5 fw-semibold">Recipient History:</label>
            <ul class="list-group" v-if="uniqueRecipientHistory.length">
              <li
                v-for="(entry, index) in uniqueRecipientHistory"
                :key="index"
                class="list-group-item d-flex justify-content-between align-items-center"
              >
                {{ entry.name }}
                <span class="badge bg-secondary">{{ entry.date }}</span>
              </li>
            </ul>
            <div v-else>
              <small class="text-muted">No recipient history</small>
            </div>
          </div>

          <!-- QR Code -->
          <div class="text-center">
            <img
              v-if="qrImage"
              :src="qrImage"
              alt="QR Code with Label"
              class="img-fluid mb-3"
              style="max-width: 200px;"
            />
            <button class="btn btn-primary" @click="downloadQR">
              Download QR Code
            </button>
          </div>
        </div>
      </div>
    </div>

    <!-- Hidden Canvas -->
    <canvas ref="qrCanvas" style="display: none;"></canvas>
  </div>
</template>

<script>
export default {
  name: "ItemDetails",
  props: {
    selectedItem: {
      type: Object,
      default: () => ({}),
    },
  },
  emits: ["edit-requested"],
  data() {
    return {
      qrImage: "",
    };
  },
  computed: {
    itemDetails() {
      return {
        "Inventory Number": this.selectedItem?.inventory_number,
        "Product Name": this.selectedItem?.product_name,
        Description: this.selectedItem?.description,
        Price: "₱ " + this.formatPrice(this.selectedItem?.price),
        "Date of Purchase": this.selectedItem?.date_of_purchase,
        "Memorandum of Receipt": this.selectedItem?.recipient,
        Classification: this.selectedItem?.classification,
        "Date Encoded": this.formatCreatedAt(this.selectedItem?.created_at),
      };
    },
    uniqueRecipientHistory() {
      const seen = new Set();
      return (this.selectedItem?.recipient_history || []).filter((entry) => {
        const key = `${entry.name}-${entry.date}`;
        if (seen.has(key)) return false;
        seen.add(key);
        return true;
      });
    },
  },
  watch: {
    selectedItem: {
      immediate: true,
      handler(newVal) {
        if (newVal?.qr_code) {
          this.generateLabeledQR();
        } else {
          this.qrImage = "";
        }
      },
    },
  },
  methods: {
    emitEditRequest() {
      this.$emit("edit-requested");
    },
    getFullImageUrl(path) {
      return `http://127.0.0.1:8000${path}`;
    },
    formatPrice(value) {
      const num = parseFloat(value) || 0;
      return new Intl.NumberFormat("en-US", {
        minimumFractionDigits: 2,
        maximumFractionDigits: 2,
      }).format(num);
    },
    formatCreatedAt(dateString) {
      if (!dateString) return "";
      const dateObj = new Date(dateString);
      return dateObj.toLocaleString("en-US", {
        month: "long",
        day: "2-digit",
        year: "numeric",
        hour: "2-digit",
        minute: "2-digit",
        second: "2-digit",
        hour12: true,
      });
    },
    async generateLabeledQR() {
      const path = this.selectedItem?.qr_code;
      const productName = this.selectedItem?.product_name || "QR Code";
      if (!path) return;

      const imageUrl = this.getFullImageUrl(path);

      const img = new Image();
      img.crossOrigin = "anonymous";

      img.onload = () => {
        const canvas = this.$refs.qrCanvas;
        const ctx = canvas.getContext("2d");

        const padding = 10;
        const fontSize = 36;
        const font = `${fontSize}px Arial`;

        canvas.width = img.width;
        canvas.height = img.height + fontSize + padding;

        ctx.fillStyle = "#FFFFFF";
        ctx.fillRect(0, 0, canvas.width, canvas.height);
        ctx.drawImage(img, 0, 0);

        ctx.font = font;
        ctx.fillStyle = "#000000";
        ctx.textAlign = "center";
        ctx.fillText(productName, canvas.width / 2, img.height + fontSize);

        this.qrImage = canvas.toDataURL("image/png");
      };

      img.src = imageUrl;
    },
    async downloadQR() {
      if (!this.qrImage) {
        await this.generateLabeledQR();
      }

      const productName = this.selectedItem?.product_name || "qr_code";
      const safeFileName = productName.replace(/[^a-zA-Z0-9_-]/g, "_");

      const link = document.createElement("a");
      link.href = this.qrImage;
      link.download = `${safeFileName}.png`;
      document.body.appendChild(link);
      link.click();
      document.body.removeChild(link);
    },
  },
};
</script>

<style scoped>
.row {
  margin-bottom: 0.5rem;
}
.text-break {
  word-break: break-word;
  white-space: pre-wrap;
}
.list-group-item {
  font-size: 14px;
}
</style>