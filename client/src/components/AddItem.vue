<template>
  <div>
    <!-- Main Add Item Modal -->
    <div class="modal fade" id="addItemModal" tabindex="-1" aria-hidden="true">
      <div class="modal-dialog modal-dialog-centered">
        <div class="modal-content p-4">
          <div class="modal-header border-0 text-center d-flex flex-column w-100">
            <h3 class="modal-title fw-bold text-center w-100">ADD ITEM</h3>
            <button type="button" class="btn-close position-absolute end-0 me-3" data-bs-dismiss="modal"></button>
          </div>

          <div class="modal-body">
            <form @submit.prevent="addItem">
              <div class="form-floating mb-3">
                <input type="text" v-model="inventoryNumber" class="form-control" placeholder="Enter Inventory Number" required />
                <label>Enter Inventory Number</label>
              </div>

              <div class="form-floating mb-3">
                <input type="text" v-model="productName" class="form-control" placeholder="Enter Product Name" required />
                <label>Enter Product Name</label>
              </div>

              <div class="form-floating mb-3">
                <input type="text" v-model="description" class="form-control" placeholder="Enter Description" />
                <label>Enter Description</label>
              </div>

              <div class="form-floating mb-3">
                <input type="number" v-model="price" class="form-control" placeholder="Enter Price" />
                <label>Enter Price</label>
              </div>

              <div class="form-floating mb-3">
                <input type="date" v-model="purchaseDate" class="form-control" placeholder="Date of Purchase" />
                <label>Date of Purchase</label>
              </div>

              <div class="form-floating mb-3">
                <input type="text" v-model="recipient" class="form-control" placeholder="Enter Recipient" />
                <label>Enter Recipient</label>
              </div>

              <div class="form-floating mb-3">
                <select v-model="classification" class="form-select">
                  <option value="SE">(SE) Semi-Expendable</option>
                  <option value="PPE">(PPE) Property, Plant & Equipment</option>
                </select>
                <label>Select Classification</label>
              </div>

              <div class="text-end">
                <button type="submit" class="btn btn-success px-4">Add Item</button>
              </div>
            </form>
          </div>
        </div>
      </div>
    </div>

    <!-- Confirmation Modal with QR Code -->
    <div class="modal fade" id="addItemSuccessModal" tabindex="-1" aria-labelledby="addItemSuccessModalLabel" aria-hidden="true">
      <div class="modal-dialog modal-dialog-centered">
        <div class="modal-content p-4">
          <div class="modal-header">
            <h5 class="modal-title" id="addItemSuccessModalLabel">Item Added</h5>
            <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close" @click="handleSuccessModalClose"></button>
          </div>
          <div class="modal-body">
            <div class="row">
              <!-- Left side: QR code -->
              <div class="col-md-6 d-flex justify-content-center align-items-center border-end">
                <img 
                  v-if="qrCodeUrl" 
                  :src="getFullImageUrl(qrCodeUrl)" 
                  alt="QR Code" 
                  class="img-fluid" 
                  width="150" 
                  height="150" 
                />
              </div>

              <!-- Right side: message and buttons -->
              <div class="col-md-6 d-flex flex-column justify-content-center align-items-end ps-4">
                <p class="mb-3 text-end w-100">Thank you! Your item has been added successfully.</p>
                <div>
                  <button v-if="qrCodeUrl" @click="downloadQR" class="btn btn-outline-primary me-2">Download QR</button>
                  <button v-if="qrCodeUrl" @click="printQR" class="btn btn-outline-secondary">Print QR</button>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { ref, onMounted } from "vue";
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
    const savedProductName = ref(""); // ✅ Store product name for download/print

    const addItem = async () => {
      if (!inventoryNumber.value) {
        alert("Please enter an inventory number.");
        return;
      }

      const checkResponse = await fetch(`http://127.0.0.1:8000/api/items/`);
      const items = await checkResponse.json();
      const duplicateItem = items.find(item => item.inventory_number === inventoryNumber.value);

      if (duplicateItem) {
        alert("Item with this inventory number already exists! Please enter a different number.");
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
        savedProductName.value = productName.value; // ✅ Save product name

        const addItemModalEl = document.getElementById("addItemModal");
        if (addItemModalEl) {
          const addItemModalInstance = Modal.getInstance(addItemModalEl);
          if (addItemModalInstance) {
            addItemModalInstance.hide();
          }
        }

        new Modal(document.getElementById("addItemSuccessModal")).show();

        emit("item-added");

        // ✅ Clear form after saving product name
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
    };

    const getFullImageUrl = (path) => {
      return `http://127.0.0.1:8000${path}`;
    };

    const downloadQR = async () => {
      if (!qrCodeUrl.value) return;
      try {
        const fullUrl = getFullImageUrl(qrCodeUrl.value);
        const response = await fetch(fullUrl);
        const blob = await response.blob();
        const blobUrl = URL.createObjectURL(blob);

        const rawName = savedProductName.value?.trim() || "qr_code";
        const safeFileName = rawName.replace(/[^a-zA-Z0-9-_]/g, "_");

        const link = document.createElement("a");
        link.href = blobUrl;
        link.download = `${safeFileName}.png`;
        document.body.appendChild(link);
        link.click();

        document.body.removeChild(link);
        URL.revokeObjectURL(blobUrl);
      } catch (error) {
        console.error("Download error:", error);
        alert("Failed to download QR code.");
      }
    };

    const printQR = () => {
      if (!qrCodeUrl.value) return;
      const imageUrl = getFullImageUrl(qrCodeUrl.value);
      const title = savedProductName.value || "QR Code";
      const printWindow = window.open("", "_blank");
      printWindow.document.write(`
        <html>
          <head>
            <title>Print QR Code</title>
          </head>
          <body style="text-align:center; padding:20px;">
            <h3>QR Code for ${title}</h3>
            <img src="${imageUrl}" style="width:200px; height:200px;" />
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
    };
  },
};
</script>
