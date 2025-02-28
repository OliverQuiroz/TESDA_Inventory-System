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
          <div class="modal-body text-center">
            <p>Thank you! Your item has been added successfully.</p>
            <img 
              v-if="qrCodeUrl" 
              :src="getFullImageUrl(qrCodeUrl)" 
              alt="QR Code" 
              class="img-fluid mt-2" 
              width="150" 
              height="150" 
            />
          </div>
          <div class="modal-footer">
            <button type="button" class="btn btn-secondary" data-bs-dismiss="modal" @click="handleSuccessModalClose">Close</button>
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

    const addItem = async () => {
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

        if (!response.ok) {
          throw new Error("Failed to add item");
        }

        const data = await response.json();
        qrCodeUrl.value = data.qr_code; // ✅ Preserve QR Code for confirmation modal

        // Hide Add Item modal
        const addItemModalEl = document.getElementById("addItemModal");
        const addItemModalInstance = Modal.getInstance(addItemModalEl);
        if (addItemModalInstance) {
          addItemModalInstance.hide();
        }

        // Show confirmation modal
        new Modal(document.getElementById("addItemSuccessModal")).show();

        // Emit event to refresh items in HomePage.vue
        emit("item-added");

        // Clear input fields BUT DO NOT reset qrCodeUrl
        inventoryNumber.value = "";
        productName.value = "";
        description.value = "";
        price.value = "";
        purchaseDate.value = "";
        recipient.value = "";
        classification.value = "";
        // ❌ Do NOT reset qrCodeUrl to preserve the QR code in the confirmation modal
      } catch (error) {
        console.error("Add item error:", error);
      }
    };

    const handleSuccessModalClose = () => {
      // Remove Bootstrap leftover backdrops
      setTimeout(() => {
        document.body.classList.remove("modal-open");
        document.querySelectorAll(".modal-backdrop").forEach(backdrop => backdrop.remove());
      }, 200);

      // ✅ Reset QR code only when the success modal is fully closed
      qrCodeUrl.value = null;
    };

    const getFullImageUrl = (path) => {
      return `http://127.0.0.1:8000${path}`;
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
      getFullImageUrl
    };
  },
};
</script>