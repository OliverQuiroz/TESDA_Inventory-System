<template>
  <div class="container mt-5" style="max-width: 600px;">
    <h3>QR Scan with @zxing/browser</h3>

    <!-- If no item scanned yet, show scanning UI -->
    <div v-if="!scannedItem">
      <!-- Start/Stop scanning buttons -->
      <div class="mb-3">
        <button
          class="btn btn-primary me-2"
          @click="startScan"
          v-if="!isScanning"
        >
          Start Scanning
        </button>
        <button
          class="btn btn-secondary"
          @click="stopScan"
          v-if="isScanning"
        >
          Stop Scanning
        </button>
      </div>

      <!-- Video preview box -->
      <div class="ratio ratio-4x3 border bg-dark" style="max-width: 100%;">
        <video
          ref="videoRef"
          style="width: 100%; height: auto;"
          playsinline
          muted
        ></video>
      </div>

      <!-- Any scan/fetch error messages -->
      <p v-if="scanError" class="alert alert-danger mt-2">
        {{ scanError }}
      </p>
    </div>

    <!-- If we successfully scanned/fetched an item, show details -->
    <div v-else class="card p-3 mt-3">
      <h5>Scanned Item Details</h5>
      <p><strong>ID:</strong> {{ scannedItem.id }}</p>
      <p><strong>Product Name:</strong> {{ scannedItem.product_name }}</p>
      <p><strong>Description:</strong> {{ scannedItem.description }}</p>
      <p><strong>Price:</strong> ₱ {{ formatPrice(scannedItem.price) }}</p>
      <p><strong>Date of Purchase:</strong> {{ scannedItem.date_of_purchase }}</p>
      <p><strong>Recipient:</strong> {{ scannedItem.recipient }}</p>
      <p><strong>Classification:</strong> {{ scannedItem.classification }}</p>

      <div v-if="scannedItem.qr_code" class="mt-2">
        <img
          :src="getFullImageUrl(scannedItem.qr_code)"
          alt="QR Code"
          width="100"
          height="100"
        />
      </div>

      <div class="mt-3">
        <button class="btn btn-info me-2" @click="editItem(scannedItem)">
          Edit Item
        </button>
        <button class="btn btn-secondary" @click="resetScan">
          Scan Again
        </button>
      </div>
    </div>
  </div>
</template>

<script>
import { ref, onBeforeUnmount } from "vue";
import { BrowserMultiFormatReader } from "@zxing/browser";

export default {
  name: "ScanZxing",
  setup() {
    const videoRef = ref(null);
    const codeReader = new BrowserMultiFormatReader();
    const isScanning = ref(false);

    // Holds the fetched item data after a successful decode
    const scannedItem = ref(null);
    const scanError = ref("");

    // Extract the item ID from the decoded text.
    // If your QR contains full details like "Inventory No: 10Product: …", 
    // this regex will extract "10". If the code is just an ID, it returns it as-is.
    const extractItemId = (decodedText) => {
      const match = decodedText.match(/Inventory\s*No:\s*(\d+)/i);
      if (match && match[1]) {
        return match[1];
      }
      return decodedText.trim();
    };

    // Start scanning with fallback logic
    const startScan = async () => {
      scanError.value = "";
      scannedItem.value = null;
      isScanning.value = true;

      try {
        // Try to use the rear camera (environment) first
        await codeReader.decodeFromVideoDevice(
          // { facingMode: "environment" },
          null,
          videoRef.value,
          onFrameDecoded
        );
      } catch (envError) {
        console.warn("Environment camera failed, fallback to user:", envError);
        try {
          // Fallback to the front camera (user)
          await codeReader.decodeFromVideoDevice(
            { facingMode: "user" },
            videoRef.value,
            onFrameDecoded
          );
        } catch (userError) {
          console.error("User camera also failed:", userError);
          scanError.value =
            "Failed to start camera. Check permissions or device camera availability.";
          isScanning.value = false;
        }
      }
    };

    // Callback for each video frame
    const onFrameDecoded = (result, error, controls) => {
      if (result) {
        console.log("Decoded text:", result.getText());
        // Extract the item ID from the decoded text
        const itemId = extractItemId(result.getText());
        console.log("Parsed item ID:", itemId);
        handleDecode(itemId);
        // Stop scanning after the first successful decode
        controls.stop();
        isScanning.value = false;
      }
      // 'error' means no QR in this frame (which is normal)
    };

    // Fetch the item data from your Django backend using the item ID
    const handleDecode = async (itemId) => {
      try {
        const res = await fetch(`http://127.0.0.1:8000/api/items/${itemId}/`);
        if (!res.ok) {
          throw new Error("Item not found or invalid QR code");
        }
        const data = await res.json();
        scannedItem.value = data;
      } catch (err) {
        console.error("Fetch item error:", err);
        scanError.value = "Could not find item for this QR code.";
      }
    };

    // Stop scanning manually
    const stopScan = () => {
      codeReader.reset();
      isScanning.value = false;
    };

    // Clear data to allow scanning again
    const resetScan = () => {
      scannedItem.value = null;
      scanError.value = "";
      // Optionally, you can automatically restart scanning here if desired
    };

    // Placeholder for your edit flow (modal or route navigation)
    const editItem = (item) => {
      alert("Open edit flow for item ID: " + item.id);
      // For example: this.$router.push(`/edit/${item.id}`);
    };

    // Format price with commas and two decimals
    const formatPrice = (value) => {
      const num = parseFloat(value) || 0;
      return new Intl.NumberFormat("en-US", {
        minimumFractionDigits: 2,
        maximumFractionDigits: 2,
      }).format(num);
    };

    // Convert a relative media path to a full URL
    const getFullImageUrl = (path) => {
      return `http://127.0.0.1:8000${path}`;
    };

    onBeforeUnmount(() => {
      codeReader.reset();
    });

    return {
      videoRef,
      isScanning,
      scannedItem,
      scanError,
      startScan,
      stopScan,
      resetScan,
      editItem,
      formatPrice,
      getFullImageUrl
    };
  }
};
</script>

<style scoped>
.container {
  min-height: 70vh;
}
</style>
