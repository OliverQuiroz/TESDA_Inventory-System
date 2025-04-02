<template>
  <!-- Item Details Modal -->
  <div
    class="modal fade"
    id="itemModal"
    tabindex="-1"
    aria-labelledby="itemModalLabel"
    aria-hidden="true"
  >
    <div class="modal-dialog">
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
            <div class="col-md-6 text-start fw-bold">
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
            <div class="col-md-6 text-start">
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
                <!-- Larger QR code -->
                <img
                  v-if="selectedItem?.qr_code"
                  :src="getFullImageUrl(selectedItem.qr_code)"
                  alt="QR Code"
                  width="200"
                  height="200"
                />
              </p>
              <p class="text-center">
                <!-- Download Button -->
                <button class="btn btn-primary" @click="downloadQR">
                  Download QR Code
                </button>
              </p>
            </div>
          </div>
        </div>
      </div>
    </div>
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
    async downloadQR() {
      if (!this.selectedItem?.qr_code) return;
      try {
        const fullUrl = this.getFullImageUrl(this.selectedItem.qr_code);
        const response = await fetch(fullUrl);
        const blob = await response.blob();
        const blobUrl = URL.createObjectURL(blob);

        // Format product name for filename
        const productName = this.selectedItem?.product_name || "qr_code";
        const safeFileName = productName.replace(/[^a-zA-Z0-9_-]/g, "_");

        // Create a temporary download link
        const link = document.createElement("a");
        link.href = blobUrl;
        link.download = `${safeFileName}.png`;
        document.body.appendChild(link);
        link.click();

        // Cleanup
        document.body.removeChild(link);
        URL.revokeObjectURL(blobUrl);
      } catch (error) {
        console.error("Download error:", error);
        alert("Failed to download QR code.");
      }
    },
  },
};
</script>
