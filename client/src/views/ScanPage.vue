<template>
  <div class="container mt-5" style="max-width: 600px;">
    <h3>QR SCAN</h3>

    <div v-if="!scannedItem">
      <div class="mb-3">
        <button class="btn btn-primary me-2" @click="startScan" v-if="!isScanning">
          Start Scanning
        </button>
        <button class="btn btn-secondary" @click="stopScan" v-if="isScanning">
          Stop Scanning
        </button>
      </div>

      <div class="ratio ratio-4x3 border bg-dark" style="max-width: 100%;">
        <video ref="videoRef" style="width: 100%; height: auto;" playsinline muted></video>
      </div>

      <p v-if="scanError" class="alert alert-danger mt-2">
        {{ scanError }}
      </p>
    </div>

    <div v-else class="card p-3 mt-3 scanned-item-container">
  <h5 class="text-center">Scanned Item Details</h5>
  <p><strong>ID:</strong> {{ scannedItem.id }}</p>
  <p><strong>Product Name:</strong> {{ scannedItem.product_name }}</p>
  <p><strong>Description:</strong> {{ scannedItem.description }}</p>
  <p><strong>Price:</strong> ₱ {{ formatPrice(scannedItem.price) }}</p>
  <p><strong>Date of Purchase:</strong> {{ scannedItem.date_of_purchase }}</p>
  <p><strong>Recipient:</strong> {{ scannedItem.recipient }}</p>
  <p><strong>Classification:</strong> {{ scannedItem.classification }}</p>

  <div v-if="scannedItem.qr_code" class="mt-2 text-center">
    <img :src="getFullImageUrl(scannedItem.qr_code)" alt="QR Code" width="100" height="100" class="border rounded">
  </div>

  <div class="mt-3 d-flex justify-content-center">
    <button class="btn btn-info me-2" @click="editItem(scannedItem)">Edit Item</button>
    <button class="btn btn-secondary" @click="resetScan">Scan Again</button>
  </div>
</div>

  </div>
</template>

<script>
import { ref, onMounted, onBeforeUnmount } from "vue";
import { BrowserMultiFormatReader } from "@zxing/browser";

export default {
  name: "ScanZxing",
  setup() {
    const videoRef = ref(null);
    let codeReader = null; // Prevent issues with re-initialization
    const isScanning = ref(false);
    const scannedItem = ref(null);
    const scanError = ref("");

    onMounted(() => {
      codeReader = new BrowserMultiFormatReader(); // Initialize on component mount
    });

    const extractItemId = (decodedText) => {
      console.log("Raw QR Code Data:", decodedText);

      const match = decodedText.match(/Inventory\s*No[:\s]+(\d+)/i);
      if (match && match[1]) {
        console.log("Extracted Item ID:", match[1]);
        return match[1];
      }

      scanError.value = "Invalid QR code format. Please scan a valid inventory QR code.";
      return null;
    };

    const startScan = async () => {
      scanError.value = "";
      scannedItem.value = null;
      isScanning.value = true;

      try {
        if (!codeReader) {
          codeReader = new BrowserMultiFormatReader(); // Ensure it's initialized
        }

        await codeReader.decodeFromVideoDevice(null, videoRef.value, onFrameDecoded);
      } catch (error) {
        console.error("Camera error:", error);
        scanError.value = "Failed to start camera. Check permissions or device camera availability.";
        isScanning.value = false;
      }
    };

    const onFrameDecoded = (result, error, controls) => {
      if (result) {
        console.log("Decoded text:", result.getText());

        const itemId = extractItemId(result.getText());
        if (!itemId) {
          console.error("Invalid QR code detected.");
          return;
        }

        handleDecode(itemId);
        controls.stop();
        isScanning.value = false;
        stopScan();
      }
    };

    const handleDecode = async (itemId) => {
      try {
        const res = await fetch(`http://127.0.0.1:8000/api/items/${itemId}/`);
        if (!res.ok) {
          throw new Error(`Item not found for ID: ${itemId}`);
        }
        const data = await res.json();
        console.log("Fetched item data:", data);
        scannedItem.value = data;
      } catch (err) {
        console.error("Fetch error:", err);
        scanError.value = "Could not find item for this QR code.";
      }
    };

    const stopScan = () => {
  if (codeReader) {
    try {
      codeReader.reset(); // Reset scanning session (doesn't always work)
    } catch (error) {
      console.warn("codeReader does not have a reset method:", error);
    }
  }

  // Properly stop the camera
  const videoElement = videoRef.value;
  if (videoElement && videoElement.srcObject) {
    const stream = videoElement.srcObject;
    stream.getTracks().forEach(track => track.stop()); // Stop all tracks
    videoElement.srcObject = null; // Clear video feed
  }

  isScanning.value = false;
};

    const resetScan = () => {
      scannedItem.value = null;
      scanError.value = "";
      isScanning.value = false; // Reset scanning state

      // Small delay to ensure the scanner resets before restarting
      setTimeout(() => {
        startScan();
      }, 500);
    };

    const editItem = (item) => {
      alert("Open edit flow for item ID: " + item.id);
    };

    const formatPrice = (value) => {
      return new Intl.NumberFormat("en-US", { minimumFractionDigits: 2, maximumFractionDigits: 2 }).format(value || 0);
    };

    const getFullImageUrl = (path) => {
      return `http://127.0.0.1:8000${path}`;
    };

    onBeforeUnmount(() => {
      if (codeReader) {
        try {
          if (typeof codeReader.reset === "function") {
            codeReader.reset();
          }
        } catch (error) {
          console.warn("Error resetting codeReader on unmount:", error);
        }
      }
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
h3 {
  text-align: center;
}

.container {
  min-height: 70vh;
}

.scanned-item-container {
  max-width: 500px;
  margin: 0 auto; /* Center the card */
  text-align: center;
}

.scanned-item-container p {
  margin-bottom: 5px; /* Reduce spacing for compact design */
}

.scanned-item-container img {
  display: block;
  margin: 0 auto; /* Center QR code */
}

.d-flex.justify-content-center {
  display: flex;
  justify-content: center;
}

</style>
