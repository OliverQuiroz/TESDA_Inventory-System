<template>
  <div>
    <!-- Add Item Modal -->
    <div class="modal fade" id="addItemModal" tabindex="-1">
      <div class="modal-dialog modal-dialog-centered modal-lg">
        <div class="modal-content p-4">
          <div class="modal-header border-0 text-center d-flex flex-column w-100">
            <h5 class="modal-title fw-bold text-center w-100">ADD ITEM</h5>
            <button type="button" class="btn-close position-absolute end-0 me-3" data-bs-dismiss="modal"></button>
          </div>

          <div class="modal-body">
            <form @submit.prevent="addItem">
              <div class="row g-3">
                <div class="col-md-6">
                  <div class="form-floating">
                    <input type="text" v-model="inventoryNumber" class="form-control" placeholder="Enter Inventory Number" required />
                    <label>Enter Inventory Number</label>
                  </div>
                </div>
                <div class="col-md-6">
                  <div class="form-floating">
                    <input type="text" v-model="productName" class="form-control" placeholder="Enter Product Name" required />
                    <label>Enter Product Name</label>
                  </div>
                </div>

                <div class="col-12">
                  <div class="form-floating">
                    <input type="text" v-model="description" class="form-control" placeholder="Enter Description" />
                    <label>Enter Description</label>
                  </div>
                </div>

                <div class="col-md-6">
                  <div class="form-floating">
                    <input type="number" v-model="price" class="form-control" placeholder="Enter Price" />
                    <label>Enter Price</label>
                  </div>
                </div>

                <div class="col-md-6">
                  <div class="form-floating">
                    <input type="date" v-model="purchaseDate" class="form-control" placeholder="Date of Purchase" />
                    <label>Date of Purchase</label>
                  </div>
                </div>

                <div class="col-md-6">
                  <div class="form-floating">
                    <input type="text" v-model="recipient" class="form-control" placeholder="Enter Recipient" />
                    <label>Enter Recipient</label>
                  </div>
                </div>

                <div class="col-md-6">
                  <div class="form-floating">
                    <select v-model="classification" class="form-select">
                      <option value="SE">(SE) Semi-Expendable</option>
                      <option value="PPE">(PPE) Property, Plant & Equipment</option>
                    </select>
                    <label>Select Classification</label>
                  </div>
                </div>
              </div>

              <div class="text-end mt-4">
                <button type="submit" class="btn btn-success w-100">Add Item</button>
              </div>
            </form>
          </div>
        </div>
      </div>
    </div>

    <!-- ✅ Success Modal (new) -->
    <div class="modal fade" id="addItemSuccessModal" tabindex="-1" aria-hidden="true">
      <div class="modal-dialog modal-dialog-centered">
        <div class="modal-content text-center p-4">
          <div class="modal-body">
            <h5 class="mb-3">Item successfully added!</h5>
            <button type="button" class="btn btn-primary w-100" data-bs-dismiss="modal">OK</button>
          </div>
        </div>
      </div>
    </div>

    <!-- Hidden Canvas for QR Label Rendering -->
    <canvas ref="qrCanvas" style="display: none;"></canvas>
  </div>
</template>

<script>
import { ref, onMounted, watch } from "vue";
import { Modal } from "bootstrap";

export default {
  name: "AddItemModal",
  emits: ["item-added"],
  setup(props, { emit }) {
    const inventoryNumber = ref("");
    const productName = ref("");
    const description = ref("");
    const price = ref("");
    const purchaseDate = ref("");
    const recipient = ref("");
    const classification = ref("");
    const qrCodeUrl = ref(null);
    const savedProductName = ref("");
    const qrCanvas = ref(null);
    const generatedQRImage = ref("");

    const addItem = async () => {
      if (!inventoryNumber.value) {
        alert("Please enter an inventory number.");
        return;
      }

      const checkResponse = await fetch(`http://127.0.0.1:8000/api/items/`);
      const items = await checkResponse.json();
      const duplicateItem = items.find(item => item.inventory_number === inventoryNumber.value);

      if (duplicateItem) {
        alert("Item with this inventory number already exists!");
        return;
      }

      const newItem = {
        inventory_number: inventoryNumber.value,
        product_name: productName.value,
        description: description.value,
        price: price.value,
        date_of_purchase: purchaseDate.value,
        recipient: recipient.value,
        classification: classification.value,
      };

      try {
        const response = await fetch("http://127.0.0.1:8000/api/items/", {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify(newItem),
        });

        const data = await response.json();

        if (!response.ok) {
          alert(data.error);
          return;
        }

        qrCodeUrl.value = data.qr_code;
        savedProductName.value = productName.value;

        const addItemModalEl = document.getElementById("addItemModal");
        if (addItemModalEl) {
          const addItemModalInstance = Modal.getInstance(addItemModalEl);
          if (addItemModalInstance) {
            addItemModalInstance.hide();
          }
        }

        new Modal(document.getElementById("addItemSuccessModal")).show();

        emit("item-added");

        inventoryNumber.value = "";
        productName.value = "";
        description.value = "";
        price.value = "";
        purchaseDate.value = "";
        recipient.value = "";
        classification.value = "";
      } catch (error) {
        console.error("Add item error:", error);
        alert("Failed to add item.");
      }
    };

    const handleSuccessModalClose = () => {
      setTimeout(() => {
        document.body.classList.remove("modal-open");
        document.querySelectorAll(".modal-backdrop").forEach(backdrop => backdrop.remove());
      }, 200);
      qrCodeUrl.value = null;
      savedProductName.value = "";
      generatedQRImage.value = "";
    };

    const getFullImageUrl = (path) => {
      return `http://127.0.0.1:8000${path}`;
    };

    const renderQRWithLabel = async () => {
      if (!qrCodeUrl.value) return;

      const imageUrl = getFullImageUrl(qrCodeUrl.value);
      const label = savedProductName.value || "QR Code";

      return new Promise((resolve) => {
        const img = new Image();
        img.crossOrigin = "anonymous";
        img.onload = () => {
          const canvas = qrCanvas.value;
          const ctx = canvas.getContext("2d");

          const padding = 20;
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
          ctx.fillText(label, canvas.width / 2, img.height + fontSize);

          const dataURL = canvas.toDataURL("image/png");
          generatedQRImage.value = dataURL;

          resolve(dataURL);
        };
        img.src = imageUrl;
      });
    };

    const downloadQR = async () => {
      const dataUrl = await renderQRWithLabel();
      if (!dataUrl) return;

      const rawName = savedProductName.value?.trim() || "qr_code";
      const safeFileName = rawName.replace(/[^a-zA-Z0-9-_]/g, "_");

      const link = document.createElement("a");
      link.href = dataUrl;
      link.download = `${safeFileName}.png`;
      document.body.appendChild(link);
      link.click();
      document.body.removeChild(link);
    };

    const printQR = async () => {
      const dataUrl = await renderQRWithLabel();
      if (!dataUrl) return;

      const title = savedProductName.value || "QR Code";
      const printWindow = window.open("", "_blank");
      printWindow.document.write(`
        <html>
          <head><title>Print QR Code</title></head>
          <body style="text-align:center; padding:20px;">
            <h3>QR Code for ${title}</h3>
            <img src="${dataUrl}" style="width:200px; height:auto;" />
            <script>
              window.onload = () => {
                window.print();
                window.onafterprint = () => window.close();
              };
            <\/script>
          </body>
        </html>
      `);
    };

    watch(qrCodeUrl, async (newVal) => {
      if (newVal) {
        await renderQRWithLabel();
      }
    });

    onMounted(() => {
      const successModalEl = document.getElementById("addItemSuccessModal");
      if (successModalEl) {
        successModalEl.addEventListener("hidden.bs.modal", handleSuccessModalClose);
      }
    });

    return {
      inventoryNumber,
      productName,
      description,
      price,
      purchaseDate,
      recipient,
      classification,
      qrCodeUrl,
      addItem,
      handleSuccessModalClose,
      getFullImageUrl,
      downloadQR,
      printQR,
      qrCanvas,
      generatedQRImage,
    };
  },
};
</script>
