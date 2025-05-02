<template>
  <div class="container mt-5" style="max-width: 1000px;">
    <h3 class="text-center fw-bold mb-4">QR SCAN - Property Number</h3>

    <div v-if="!scannedItem">
      <div class="d-flex justify-content-center mb-3 gap-2">
        <button class="btn btn-primary btn-sm" @click="startScan" v-if="!isScanning">
          <i class="bi bi-camera"></i> Start Scanning
        </button>
        <button class="btn btn-secondary btn-sm" @click="stopScan" v-else>
          <i class="bi bi-stop-circle"></i> Stop Scanning
        </button>
      </div>

      <div class="d-flex justify-content-center">
        <div class="ratio ratio-4x3 border rounded bg-dark overflow-hidden" style="width: 600px;">
          <video ref="videoRef" class="w-100 h-100" playsinline muted></video>
        </div>
      </div>

      <p v-if="scanError" class="alert alert-danger mt-3 text-center small mb-0">
        {{ scanError }}
      </p>
    </div>

    <div v-else class="card mt-4 shadow-sm p-4">
      <h5 class="fw-bold text-center mb-4">Scanned Item Details</h5>
      <div class="row">
        <!-- LEFT COLUMN: ITEM DETAILS -->
        <div class="col-md-8">
          <div class="row mb-2"><div class="col-5 fw-semibold">Date of Acquisition:</div><div class="col-7 text-break">{{ formatDate(scannedItem.date_of_acquisition) }}</div></div>
          <div class="row mb-2"><div class="col-5 fw-semibold">Accountable Person:</div><div class="col-7 text-break">{{ scannedItem.accountable_person }}</div></div>
          <div class="row mb-2"><div class="col-5 fw-semibold">Fund:</div><div class="col-7 text-break">{{ scannedItem.fund }}</div></div>
          <div class="row mb-2"><div class="col-5 fw-semibold">Article:</div><div class="col-7 text-break">{{ scannedItem.article }}</div></div>
          <div class="row mb-2"><div class="col-5 fw-semibold">Description:</div><div class="col-7 text-break">{{ scannedItem.description }}</div></div>
          <div class="row mb-2"><div class="col-5 fw-semibold">UACS Code:</div><div class="col-7">{{ scannedItem.uacs_code }}</div></div>
          <div class="row mb-2"><div class="col-5 fw-semibold">Category (UACS):</div><div class="col-7">{{ scannedItem.uacs_category }}</div></div>
          <div class="row mb-2"><div class="col-5 fw-semibold">Unit Cost:</div><div class="col-7">₱ {{ formatPrice(scannedItem.unit_cost) }}</div></div>
          <div class="row mb-2"><div class="col-5 fw-semibold">Quantity:</div><div class="col-7">{{ scannedItem.quantity }}</div></div>
          <div class="row mb-2"><div class="col-5 fw-semibold">Total Cost:</div><div class="col-7">₱ {{ formatPrice(scannedItem.total_cost) }}</div></div>
          <div class="row mb-2"><div class="col-5 fw-semibold">Unit:</div><div class="col-7">{{ scannedItem.unit }}</div></div>
          <div class="row mb-2"><div class="col-5 fw-semibold">Location:</div><div class="col-7">{{ scannedItem.location }}</div></div>
          <div class="row mb-2"><div class="col-5 fw-semibold">Property Number:</div><div class="col-7">{{ scannedItem.property_number }}</div></div>
          <div class="row mb-2"><div class="col-5 fw-semibold">ICS Number:</div><div class="col-7">{{ scannedItem.ics_number }}</div></div>
          <div class="row mb-2"><div class="col-5 fw-semibold">Date of PO:</div><div class="col-7">{{ formatDate(scannedItem.date_of_po) }}</div></div>
          <div class="row mb-2"><div class="col-5 fw-semibold">PO Number:</div><div class="col-7">{{ scannedItem.po_number }}</div></div>
          <div class="row mb-3"><div class="col-5 fw-semibold">Supplier:</div><div class="col-7">{{ scannedItem.supplier_name }}</div></div>
        </div>

        <!-- RIGHT COLUMN: QR + BUTTONS -->
        <div class="col-md-4 text-center">
          <img
            v-if="scannedItem.qr_code"
            :src="getFullImageUrl(scannedItem.qr_code)"
            alt="QR Code"
            class="img-fluid border p-1 mb-3"
            style="max-width: 200px;"
          />
          <div class="d-flex justify-content-center gap-2">
            <button class="btn btn-outline-info btn-sm" @click="openEditModal(scannedItem)">
              <i class="bi bi-pencil-square"></i> Edit Item
            </button>
            <button class="btn btn-secondary btn-sm" @click="resetScan">
              <i class="bi bi-arrow-repeat"></i> Scan Again
            </button>
          </div>
        </div>
      </div>
    </div>

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

    onMounted(() => {
      codeReader = new BrowserMultiFormatReader();
    });

    const extractPropertyNumber = (decodedText) => {
  console.log("Raw QR Code Data:", decodedText);

  const match = decodedText.match(/(?:Inventory|Property)\s*(?:Number|No)\.?\s*[:：]?\s*([^\r\n]+)/i);

  if (match && match[1]) {
    const propNo = match[1].split("\n")[0].trim();
    console.log("Extracted Property Number:", propNo);
    return propNo;
  }

  scanError.value = "Invalid QR code format. Please ensure the code has 'Property No: <text>'.";
  return null;
};


    const startScan = async () => {
      scanError.value = "";
      scannedItem.value = null;
      isScanning.value = true;

      try {
        if (!codeReader) codeReader = new BrowserMultiFormatReader();
        await codeReader.decodeFromVideoDevice(null, videoRef.value, onFrameDecoded);
      } catch (error) {
        scanError.value = "Failed to access camera.";
        isScanning.value = false;
      }
    };

    const onFrameDecoded = (result, error, controls) => {
      if (result) {
        const propNo = extractPropertyNumber(result.getText());
        if (!propNo) return;
        fetchItemByPropertyNumber(propNo);
        controls.stop();
        isScanning.value = false;
        stopScan();
      }
    };

    const fetchItemByPropertyNumber = async (propNo) => {
      try {
        const res = await fetch(`http://127.0.0.1:8000/api/items/?property_number=${encodeURIComponent(propNo)}`);
        const data = await res.json();
        if (!Array.isArray(data) || data.length === 0) throw new Error();
        scannedItem.value = data[0];
      } catch {
        scanError.value = "Could not find an item for this property number.";
      }
    };

    const stopScan = () => {
      if (codeReader) {
        try {
          codeReader.reset();
        } catch (err) {
          console.warn("codeReader reset error:", err);
        }
      }
      if (videoRef.value?.srcObject) {
        videoRef.value.srcObject.getTracks().forEach((track) => track.stop());
        videoRef.value.srcObject = null;
      }
      isScanning.value = false;
    };

    const resetScan = () => {
      scannedItem.value = null;
      scanError.value = "";
      isScanning.value = false;
    };

    const openEditModal = (item) => {
      selectedItem.value = item;
      setTimeout(() => {
        const modalEl = document.getElementById("editItemModal");
        if (!modalEl) return;
        new Modal(modalEl, { backdrop: "static" }).show();
      }, 100);
    };

    const fetchUpdatedItem = () => {
      if (scannedItem.value?.property_number) {
        fetchItemByPropertyNumber(scannedItem.value.property_number);
      }
    };

    const formatPrice = (val) => {
      return new Intl.NumberFormat("en-PH", { minimumFractionDigits: 2 }).format(parseFloat(val || 0));
    };

    const formatDate = (raw) => {
      if (!raw) return "";
      return new Date(raw).toLocaleDateString("en-GB", { day: "2-digit", month: "short", year: "numeric" });
    };

    const getFullImageUrl = (path) => `http://127.0.0.1:8000${path}`;

    onBeforeUnmount(() => stopScan());

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
      formatDate,
      getFullImageUrl,
    };
  },
};
</script>

<style scoped>
.container {
  min-height: 70vh;
}
.card-header {
  background-color: #f8f9fa;
}
</style>
