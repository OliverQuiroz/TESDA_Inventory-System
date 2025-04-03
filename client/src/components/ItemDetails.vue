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
          <div class="row">
            <!-- Labels Column -->
            <div class="col-md-6 col-12 fw-bold">
              <p>Inventory Number:</p>
              <p>Product Name:</p>
              <p>Description:</p>
              <p>Price:</p>
              <p>Date of Purchase:</p>
              <p>Memorandum of Receipt:</p>
              <p>Classification:</p>
              <p>Date Encoded:</p>
              <p>QR Code:</p>
            </div>

            <!-- Data Column -->
            <div class="col-md-6 col-12">
              <p>{{ selectedItem?.inventory_number }}</p>
              <p>{{ selectedItem?.product_name }}</p>
              <p>{{ selectedItem?.description }}</p>
              <p>₱ {{ formatPrice(selectedItem?.price) }}</p>
              <p>{{ selectedItem?.date_of_purchase }}</p>
              <p>{{ selectedItem?.recipient }}</p>
              <p>{{ selectedItem?.classification }}</p>

              <!-- Format the created_at field for a more readable display -->
              <p>{{ formatCreatedAt(selectedItem?.created_at) }}</p>

              <p class="text-center">
                <img
                  v-if="qrImage"
                  :src="qrImage"
                  alt="QR Code with Label"
                  width="200"
                  height="auto"
                />
              </p>
              <p class="text-center">
                <button class="btn btn-primary" @click="downloadQR">
                  Download QR Code
                </button>
              </p>
            </div>
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
      qrImage: "", // Holds the canvas-rendered QR image with label
    };
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

      // Convert the ISO string to a JavaScript Date object
      const dateObj = new Date(dateString);

      // Example format: "April 02, 2025, 3:59:53 PM"
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
