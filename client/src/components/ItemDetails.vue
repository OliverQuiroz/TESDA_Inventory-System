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
                <p>
                  <!-- Clickable QR image -->
                  <img
                    v-if="selectedItem?.qr_code"
                    :src="getFullImageUrl(selectedItem.qr_code)"
                    alt="QR Code"
                    width="100"
                    height="100"
                    style="cursor: pointer;"
                    @click="openQrModal"
                  />
                </p>
              </div>
            </div>
          </div>
          <div class="modal-footer">
            <!-- Button triggers EditItem modal in parent (HomePage, etc.) -->
            <button
              type="button"
              class="btn btn-info"
              @click="emitEditRequest"
              data-bs-dismiss="modal"
            >
              <i class="bi bi-pencil"></i> Edit
            </button>
          </div>
        </div>
      </div>
    </div>
  
    <!-- Larger QR Code Preview Modal -->
    <div
      class="modal fade"
      id="qrLargeModal"
      tabindex="-1"
      aria-labelledby="qrLargeModalLabel"
      aria-hidden="true"
    >
      <div class="modal-dialog modal-dialog-centered">
        <div class="modal-content p-4">
          <div class="modal-header">
            <h5 class="modal-title" id="qrLargeModalLabel">QR Code Preview</h5>
            <button
              type="button"
              class="btn-close"
              data-bs-dismiss="modal"
              aria-label="Close"
            ></button>
          </div>
          <div class="modal-body text-center">
            <img
              v-if="selectedItem?.qr_code"
              :src="getFullImageUrl(selectedItem.qr_code)"
              alt="QR Code"
              style="max-width: 80%; max-height: 80vh;"
            />
          </div>
          <div class="modal-footer">
            <button 
              class="btn btn-secondary" 
              data-bs-dismiss="modal"
            >
              Close
            </button>
            <!-- Download triggers a forced download via Blob technique -->
            <button 
              class="btn btn-primary" 
              @click="downloadQR"
            >
              Download
            </button>
          </div>
        </div>
      </div>
    </div>
  </template>
  
  <script>
  import { Modal } from "bootstrap";
  
  export default {
    name: "ItemDetails",
    props: {
      // The selected item to display
      selectedItem: {
        type: Object,
        default: () => ({}),
      },
    },
    emits: ["edit-requested"],
    methods: {
      // Let parent know the user clicked "Edit"
      emitEditRequest() {
        this.$emit("edit-requested");
      },
      // Convert relative path (e.g. "/media/qr_codes/10_qr.png") to full URL
      getFullImageUrl(path) {
        return `http://127.0.0.1:8000${path}`;
      },
      // Nicely format price with commas
      formatPrice(value) {
        const num = parseFloat(value) || 0;
        return new Intl.NumberFormat("en-US", {
          minimumFractionDigits: 2,
          maximumFractionDigits: 2,
        }).format(num);
      },
      // Show the larger QR code modal
      openQrModal() {
        const modalEl = document.getElementById("qrLargeModal");
        if (!modalEl) return;
        const modal = new Modal(modalEl);
        modal.show();
      },
      // Force a direct download of the QR image
      async downloadQR() {
        if (!this.selectedItem?.qr_code) return;
        try {
          // 1) Fetch image as a Blob
          const fullUrl = this.getFullImageUrl(this.selectedItem.qr_code);
          const response = await fetch(fullUrl);
          const blob = await response.blob();
  
          // 2) Create a temporary Blob URL
          const blobUrl = URL.createObjectURL(blob);
  
          // 3) Programmatically create an <a> and click it to download
          const link = document.createElement("a");
          link.href = blobUrl;
          link.download = "qr_code.png"; // rename as desired
          document.body.appendChild(link);
          link.click();
  
          // 4) Cleanup
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
  
  <!-- Optional styling -->
  <!--
  <style scoped>
  </style>
  -->
  
  