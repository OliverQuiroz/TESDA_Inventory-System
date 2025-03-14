<template>
  <div class="container mt-5" style="max-width: 600px;">
    <h3 class="text-center">QR SCAN</h3>

    <!-- If we haven't scanned an item yet, show scanning UI -->
    <div v-if="!scannedItem">
      <div class="d-flex justify-content-center mb-3">
        <!-- Start/Stop scanning buttons -->
        <button class="btn btn-primary" @click="startScan" v-if="!isScanning">
          Start Scanning
        </button>
        <button class="btn btn-secondary" @click="stopScan" v-else>
          Stop Scanning
        </button>
      </div>

      <!-- Video preview -->
      <div class="ratio ratio-4x3 border bg-dark" style="max-width: 100%;">
        <video
          ref="videoRef"
          style="width: 100%; height: auto;"
          playsinline
          muted
        ></video>
      </div>

      <!-- Any errors -->
      <p v-if="scanError" class="alert alert-danger mt-2 text-center">
        {{ scanError }}
      </p>
    </div>

    <!-- Once we've scanned/fetched the item, show its details -->
    <div v-else class="card p-3 mt-3 scanned-item-container">
      <h5 class="text-center">Scanned Item Details</h5>
      <p><strong>Inventory Number:</strong> {{ scannedItem.inventory_number }}</p>
      <p><strong>Product Name:</strong> {{ scannedItem.product_name }}</p>
      <p><strong>Description:</strong> {{ scannedItem.description }}</p>
      <p><strong>Price:</strong> ₱ {{ formatPrice(scannedItem.price) }}</p>
      <p><strong>Date of Purchase:</strong> {{ scannedItem.date_of_purchase }}</p>
      <p><strong>Recipient:</strong> {{ scannedItem.recipient }}</p>
      <p><strong>Classification:</strong> {{ scannedItem.classification }}</p>

      <div v-if="scannedItem.qr_code" class="mt-2 text-center">
        <img
          :src="getFullImageUrl(scannedItem.qr_code)"
          alt="QR Code"
          width="100"
          height="100"
          class="border rounded"
        />
      </div>

      <div class="mt-3 d-flex justify-content-center">
        <button class="btn btn-info me-2" @click="openEditModal(scannedItem)">
          Edit Item
        </button>
        <button class="btn btn-secondary" @click="resetScan">
          Scan Again
        </button>
      </div>
    </div>

    <!-- Example EditItem modal (if you have it) -->
    <EditItem :selectedItem="selectedItem" @item-updated="fetchUpdatedItem" />
  </div>
</template>

<script>
import { ref, onMounted, onBeforeUnmount } from "vue";
import { BrowserMultiFormatReader } from "@zxing/browser";
import EditItem from "@/components/EditItem.vue";
import { Modal } from "bootstrap";

export default {
  name: "ScanZxing",
  components: { EditItem },
  setup() {
    const videoRef = ref(null);
    let codeReader = null;

    const isScanning = ref(false);
    const scannedItem = ref(null);
    const scanError = ref("");
    const selectedItem = ref(null);

    // On mount, create the codeReader instance
    onMounted(() => {
      codeReader = new BrowserMultiFormatReader();
    });

    // Regex to extract the inventory number from text like "Inventory No: 11"
    const extractInventoryNumber = (decodedText) => {
      console.log("Raw QR Code Data:", decodedText);

      // E.g. "Inventory No: 11" or "Inventory Number: 11"
      const match = decodedText.match(/Inventory\s*(?:Number|No)\s*[:\s]+(\d+)/i);
      if (match && match[1]) {
        console.log("Extracted Inventory Number:", match[1]);
        return match[1];
      }
      scanError.value =
        "Invalid QR code format. Please ensure the code has 'Inventory No: <num>'.";
      return null;
    };

    // Start scanning (try environment camera, then fallback)
    const startScan = async () => {
      scanError.value = "";
      scannedItem.value = null;
      isScanning.value = true;

      try {
        if (!codeReader) {
          codeReader = new BrowserMultiFormatReader();
        }

        // Attempt rear camera first
        await codeReader.decodeFromVideoDevice(
          { facingMode: "environment" },
          videoRef.value,
          onFrameDecoded
        );
      } catch (envError) {
        console.warn("Environment camera failed, fallback to user:", envError);
        try {
          // Fallback to front camera
          await codeReader.decodeFromVideoDevice(
            // { facingMode: "user" },
            null,
            videoRef.value,
            onFrameDecoded
          );
        } catch (userError) {
          console.error("Camera error:", userError);
          scanError.value =
            "Failed to start camera. Check permissions or device camera availability.";
          isScanning.value = false;
        }
      }
    };

    // Called for each frame
    const onFrameDecoded = (result, error, controls) => {
      if (result) {
        console.log("Decoded text:", result.getText());

        const invNumber = extractInventoryNumber(result.getText());
        if (!invNumber) {
          console.error("Invalid QR code detected.");
          return;
        }

        // If we got a valid inventory number, fetch item by it
        fetchItemByInventoryNumber(invNumber);

        // Stop scanning after success
        controls.stop();
        isScanning.value = false;
        stopScan();
      }
      // 'error' is normal if no code in that frame
    };

    // Actually fetch item by inventory_number => /api/items/?inventory_number=11
    const fetchItemByInventoryNumber = async (invNumber) => {
      try {
        const res = await fetch(`http://127.0.0.1:8000/api/items/?inventory_number=${invNumber}`);
        if (!res.ok) {
          throw new Error(`No item found for Inventory Number: ${invNumber}`);
        }
        const data = await res.json();
        if (!Array.isArray(data) || data.length === 0) {
          throw new Error("No items match that inventory_number.");
        }

        console.log("Fetched item data:", data[0]);
        scannedItem.value = data[0];
      } catch (err) {
        console.error("Fetch error:", err);
        scanError.value = "Could not find an item for this inventory number.";
      }
    };

    // Stop scanning
    const stopScan = () => {
      if (codeReader) {
        try {
          codeReader.reset();
        } catch (error) {
          console.warn("codeReader reset error:", error);
        }
      }
      const videoElement = videoRef.value;
      if (videoElement && videoElement.srcObject) {
        const stream = videoElement.srcObject;
        stream.getTracks().forEach((track) => track.stop());
        videoElement.srcObject = null;
      }
      isScanning.value = false;
    };

    // Clear data so we can scan again
    const resetScan = () => {
      scannedItem.value = null;
      scanError.value = "";
      isScanning.value = false;
    };

    // Open the edit modal if needed
    const openEditModal = (item) => {
      selectedItem.value = item;
      setTimeout(() => {
        const editModalEl = document.getElementById("editItemModal");
        if (!editModalEl) {
          console.error("Error: EditItem modal element not found!");
          return;
        }
        const editModal = new Modal(editModalEl, { backdrop: "static" });
        editModal.show();
      }, 100);
    };

    // After editing, re-fetch if needed
    const fetchUpdatedItem = () => {
      if (scannedItem.value?.inventory_number) {
        fetchItemByInventoryNumber(scannedItem.value.inventory_number);
      }
    };

    // Format currency
    const formatPrice = (value) => {
      return new Intl.NumberFormat("en-US", {
        minimumFractionDigits: 2,
        maximumFractionDigits: 2,
      }).format(value || 0);
    };

    // Build absolute URL for QR code image
    const getFullImageUrl = (path) => {
      return `http://127.0.0.1:8000${path}`;
    };

    onBeforeUnmount(() => {
      stopScan();
    });

    return {
      videoRef,
      isScanning,
      scannedItem,
      scanError,
      selectedItem,

      startScan,
      stopScan,
      resetScan,
      openEditModal,
      fetchUpdatedItem,

      formatPrice,
      getFullImageUrl
    };
  },
};
</script>

<style scoped>
h3 {
  text-align: center;
}
.container {
  min-height: 70vh;
}
.scanned-item-container {
  max-width: 500px;
  margin: 0 auto;
  text-align: center;
}
.scanned-item-container p {
  margin-bottom: 5px;
}
.scanned-item-container img {
  display: block;
  margin: 0 auto;
}
</style>
