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
        <div class="modal-header border-0 d-flex flex-column w-100 text-center">
          <h5 class="modal-title fw-bold w-100">ITEM DETAILS</h5>
          <button
            class="btn-close position-absolute end-0 me-3"
            data-bs-dismiss="modal"
          ></button>
        </div>

        <div class="modal-body">
          <!-- key/value pairs -->
          <div
            v-for="(value, label) in itemDetails"
            :key="label"
            class="row mb-2"
          >
            <div class="col-sm-5 fw-semibold">{{ label }}:</div>
            <div class="col-sm-7 text-break">{{ value }}</div>
          </div>

          <!-- Accountable-person history -->
          <div class="mb-4">
            <label class="fw-semibold">Accountable History:</label>
            <ul
              v-if="uniqueAccountableHistory.length"
              class="list-group mt-1"
            >
              <li
                v-for="(entry, idx) in uniqueAccountableHistory"
                :key="idx"
                class="list-group-item d-flex justify-content-between align-items-center"
              >
                {{ entry.name }}
                <span class="badge bg-secondary">{{ entry.date }}</span>
              </li>
            </ul>
            <small v-else class="text-muted">No history available</small>
          </div>

          <!-- QR code preview & download -->
          <div class="text-center">
            <img
              v-if="qrImage"
              :src="qrImage"
              alt="QR Code"
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

    <!-- hidden canvas -->
    <canvas ref="qrCanvas" style="display:none"></canvas>
  </div>
</template>

<script>
export default {
  name: "ItemDetails",
  props: {
    selectedItem: { type: Object, default: () => ({}) },
  },
  emits: ["edit-requested"],

  data() {
    return { qrImage: "" };
  },

  /* ---------- computed ---------- */
  computed: {
    itemDetails() {
      return {
        "Date of Acquisition":  this.selectedItem?.date_of_acquisition,
        "Accountable Person":   this.selectedItem?.accountable_person,
        Fund:                   this.selectedItem?.fund,
        Article:                this.selectedItem?.article,
        Description:            this.selectedItem?.description,
        "UACS Code":            this.selectedItem?.uacs_code,
        "Category (UACS)":      this.selectedItem?.uacs_category,
        "Unit Cost":            "₱ " + this.formatNumber(this.selectedItem?.unit_cost),
        Quantity:               this.selectedItem?.quantity,
        "Total Cost":           "₱ " + this.formatNumber(this.selectedItem?.total_cost),
        Unit:                   this.selectedItem?.unit,
        Location:               this.selectedItem?.location,
        "Property Number":      this.selectedItem?.property_number,
        "ICS No.":              this.selectedItem?.ics_number,
        "Date of PO":           this.selectedItem?.date_of_po,
        "PO #":                 this.selectedItem?.po_number,
        "Supplier Name":        this.selectedItem?.supplier_name,
        "Date Encoded":         this.formatTimestamp(this.selectedItem?.created_at),
      };
    },

    uniqueAccountableHistory() {
      const seen = new Set();
      return (this.selectedItem?.accountable_history || []).filter((e) => {
        const k = `${e.name}-${e.date}`;
        if (seen.has(k)) return false;
        seen.add(k);
        return true;
      });
    },
  },

  /* ---------- watchers ---------- */
  watch: {
    selectedItem: {
      immediate: true,
      handler(v) {
        if (v?.qr_code) this.generateLabeledQR();
        else this.qrImage = "";
      },
    },
  },

  /* ---------- methods ---------- */
  methods: {
    emitEditRequest() { this.$emit("edit-requested"); },

    apiPath(p) { return `http://127.0.0.1:8000${p}`; },

    formatNumber(v) {
      return new Intl.NumberFormat("en-US", {
        minimumFractionDigits: 2,
        maximumFractionDigits: 2,
      }).format(parseFloat(v) || 0);
    },

    formatTimestamp(ts) {
      if (!ts) return "";
      return new Date(ts).toLocaleString("en-US", {
        month:  "long",
        day:    "2-digit",
        year:   "numeric",
        hour:   "2-digit",
        minute: "2-digit",
        second: "2-digit",
        hour12: true,
      });
    },

    /* ---- QR helpers ---- */
    async generateLabeledQR() {
  const qrPath = this.selectedItem?.qr_code;
  const itemLabel = this.selectedItem?.article || "QR Code";
  const headerLabel = "TESDA JGMZSAT";
  if (!qrPath) return;

  const img = new Image();
  img.crossOrigin = "anonymous";
  img.onload = () => {
    const canvas = this.$refs.qrCanvas;
    const ctx = canvas.getContext("2d");

    // 3x4 inches portrait at 96 DPI
    const targetWidth = 288;
    const targetHeight = 384;
    const padding = 10;
    const fSize = 20;

    canvas.width = targetWidth;
    canvas.height = targetHeight;

    ctx.fillStyle = "#fff";
    ctx.fillRect(0, 0, canvas.width, canvas.height);

    // Header label
    ctx.font = `${fSize}px Arial`;
    ctx.fillStyle = "#000";
    ctx.textAlign = "center";
    ctx.fillText(headerLabel, canvas.width / 2, padding + fSize); // top center text

    // Wrap item label (bottom text)
    const maxLabelLength = 25;
    const labelLines = itemLabel.length > maxLabelLength
      ? [itemLabel.slice(0, maxLabelLength), itemLabel.slice(maxLabelLength)]
      : [itemLabel];

    // Bottom label height
    const labelBlockHeight = labelLines.length * fSize;

    // Reserve header + footer space
    const spaceAboveQR = padding + fSize + 10;
    const spaceBelowQR = padding + labelBlockHeight + 10;

    // Make QR size as big as possible but fit remaining vertical space
    const availableHeight = targetHeight - spaceAboveQR - spaceBelowQR;
    const qrSize = Math.min(targetWidth * 0.8, availableHeight); // 80% width or vertical fit
    const qrX = (targetWidth - qrSize) / 2;
    const qrY = spaceAboveQR + ((availableHeight - qrSize) / 2); // center in vertical space

    ctx.drawImage(img, qrX, qrY, qrSize, qrSize);

    // Draw bottom label
    labelLines.forEach((line, i) => {
      const lineY = targetHeight - padding - ((labelLines.length - i - 1) * fSize);
      ctx.fillText(line, canvas.width / 2, lineY);
    });

    this.qrImage = canvas.toDataURL("image/png");
  };

  img.src = this.apiPath(qrPath);
},




    async downloadQR() {
      if (!this.qrImage) await this.generateLabeledQR();
      const name = (this.selectedItem?.article || "qr_code").replace(/[^a-z0-9_-]/gi,"_");
      const a    = document.createElement("a");
      a.href     = this.qrImage;
      a.download = `${name}.png`;
      document.body.appendChild(a);
      a.click();
      document.body.removeChild(a);
    },
  },
};
</script>

<style scoped>
.row        { margin-bottom: 0.5rem; }
.text-break { word-break: break-word; white-space: pre-wrap; }
.list-group-item { font-size: 14px; }
</style>
