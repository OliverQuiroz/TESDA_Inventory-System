<template>
  <div>
    <!-- Main Add Item Modal -->
    <div
      class="modal fade"
      id="addItemModal"
      tabindex="-1"
      aria-hidden="true"
    >
      <div class="modal-dialog modal-dialog-centered">
        <div class="modal-content p-4">
          <div class="modal-header border-0 text-center d-flex flex-column w-100">
            <h3 class="modal-title fw-bold text-center w-100">ADD ITEM</h3>
            <button
              type="button"
              class="btn-close position-absolute end-0 me-3"
              data-bs-dismiss="modal"
            ></button>
          </div>

          <div class="modal-body">
            <form @submit.prevent="addItem">
              <div class="form-floating mb-3">
                <input
                  type="text"
                  v-model="inventoryNumber"
                  class="form-control"
                  placeholder="Enter Inventory Number"
                />
                <label>Enter Inventory Number</label>
              </div>

              <div class="form-floating mb-3">
                <input
                  type="text"
                  v-model="productName"
                  class="form-control"
                  placeholder="Enter Product Name"
                />
                <label>Enter Product Name</label>
              </div>

              <div class="form-floating mb-3">
                <input
                  type="text"
                  v-model="description"
                  class="form-control"
                  placeholder="Enter Description"
                />
                <label>Enter Description</label>
              </div>

              <div class="form-floating mb-3">
                <input
                  type="number"
                  v-model="price"
                  class="form-control"
                  placeholder="Enter Price"
                />
                <label>Enter Price</label>
              </div>

              <div class="form-floating mb-3">
                <input
                  type="date"
                  v-model="purchaseDate"
                  class="form-control"
                  placeholder="Date of Purchase"
                />
                <label>Date of Purchase</label>
              </div>

              <div class="form-floating mb-3">
                <input
                  type="text"
                  v-model="recipient"
                  class="form-control"
                  placeholder="Enter Recipient"
                />
                <label>Enter Recipient</label>
              </div>

              <div class="form-floating mb-3">
                <!-- If your backend expects "SE"/"PPE", replace with those. -->
                <select v-model="classification" class="form-select">
                  <option value="SE">(SE) Semi-Expendable</option>
                  <option value="PPE">(PPE) Property, Plant & Equipment</option>
                </select>
                <label>Select Classification</label>
              </div>

              <div class="text-end">
                <button type="submit" class="btn btn-success px-4">
                  Add Item
                </button>
              </div>
            </form>
          </div>
        </div>
      </div>
    </div>

    <!-- Confirmation Modal (Thank you style) -->
    <div
      class="modal fade"
      id="addItemSuccessModal"
      tabindex="-1"
      aria-labelledby="addItemSuccessModalLabel"
      aria-hidden="true"
    >
      <div class="modal-dialog modal-dialog-centered">
        <div class="modal-content p-4">
          <div class="modal-header">
            <h5 class="modal-title" id="addItemSuccessModalLabel">
              Item Added
            </h5>
            <button
              type="button"
              class="btn-close"
              data-bs-dismiss="modal"
              aria-label="Close"
            ></button>
          </div>
          <div class="modal-body">
            Thank you! Your item has been added successfully.
          </div>
          <!-- <div class="modal-footer">
            <button
              type="button"
              class="btn btn-secondary"
              data-bs-dismiss="modal"
              @click="handleSuccessModalClose"
            >
              Close
            </button>
          </div> -->
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

    // Force removal of leftover backdrop & modal-open classes
    const removeModalBackdrop = () => {
      const modalsOpen = document.querySelectorAll(".modal.show");
      if (modalsOpen.length === 0) {
        // If no modals are open, remove .modal-open & any leftover .modal-backdrop
        document.body.classList.remove("modal-open");
        const backdrop = document.querySelector(".modal-backdrop");
        if (backdrop) {
          backdrop.remove();
        }
      }
    };

    onMounted(() => {
      // Listen for hide on success modal, then remove leftover backdrop
      const successModalEl = document.getElementById("addItemSuccessModal");
      successModalEl.addEventListener("hidden.bs.modal", removeModalBackdrop);
    });

    const handleSuccessModalClose = () => {
      removeModalBackdrop();
    };

    const addItem = async () => {
      if (!inventoryNumber.value || !productName.value || !classification.value) {
        alert("Please fill in all required fields.");
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

        if (!response.ok) {
          const errorData = await response.json();
          console.error("Add item error:", errorData);
          alert("Failed to add item.");
          return;
        }

        const data = await response.json();
        console.log("Item added:", data);

        // 1) Hide the "Add Item" modal
        const addModalEl = document.getElementById("addItemModal");
        const addItemModal = Modal.getInstance(addModalEl);
        if (addItemModal) {
          addItemModal.hide();
        }

        // 2) Show success/thank-you modal
        const successModalEl = document.getElementById("addItemSuccessModal");
        const successModal = new Modal(successModalEl);
        successModal.show();

        // 3) Clear form fields
        inventoryNumber.value = "";
        productName.value = "";
        description.value = "";
        price.value = "";
        purchaseDate.value = "";
        recipient.value = "";
        classification.value = "";

        // 4) Emit event so parent can refresh the table
        emit("item-added");
      } catch (error) {
        console.error("Add item error:", error);
        alert("An error occurred while adding the item.");
      }
    };

    return {
      inventoryNumber,
      productName,
      description,
      price,
      purchaseDate,
      recipient,
      classification,
      addItem,
      handleSuccessModalClose,
    };
  },
};
</script>

<style scoped src="./AddItemModalStyles.css"></style>
