<template>
    <div class="modal fade" id="editItemModal" tabindex="-1" ref="editModal">
      <div class="modal-dialog">
        <div class="modal-content p-4">
          <div class="modal-header border-0 text-center d-flex flex-column w-100">
            <h5 class="modal-title fw-bold text-center w-100">EDIT ITEM</h5>
            <button
              type="button"
              class="btn-close position-absolute end-0 me-3"
              data-bs-dismiss="modal"
            ></button>
          </div>
          <div class="modal-body">
            <form @submit.prevent="validateAndUpdateItem">
              <div class="mb-3">
                <label>Product Name</label>
                <input
                  type="text"
                  class="form-control"
                  v-model.trim="editedItem.product_name"
                  required
                />
              </div>
              <div class="mb-3">
                <label>Description</label>
                <textarea
                  class="form-control"
                  v-model.trim="editedItem.description"
                  required
                ></textarea>
              </div>
              <div class="mb-3">
                <label>Price</label>
                <input
                  type="number"
                  class="form-control"
                  v-model="editedItem.price"
                  min="1"
                  required
                />
              </div>
              <div class="mb-3">
                <label>Date of Purchase</label>
                <input
                  type="date"
                  class="form-control"
                  v-model="editedItem.date_of_purchase"
                  required
                />
              </div>
              <div class="mb-3">
                <label>Transfer to</label>
                <input
                  type="text"
                  class="form-control"
                  v-model.trim="editedItem.recipient"
                  required
                />
              </div>
              <div class="mb-3">
                <label>Classification</label>
                <select
                  class="form-control"
                  v-model="editedItem.classification"
                  required
                >
                  <option value="PPE">PPE</option>
                  <option value="SE">SE</option>
                </select>
              </div>
              <div class="modal-footer">
                <button type="submit" class="btn btn-success">
                  Save Changes
                </button>
              </div>
            </form>
          </div>
        </div>
      </div>
    </div>
  </template>
  
  <script>
  import { Modal } from "bootstrap";
  import { nextTick } from "vue";
  
  export default {
    props: ["selectedItem"],
    data() {
      return {
        editedItem: {},
        modalInstance: null,
      };
    },
    watch: {
      selectedItem: {
        handler(newVal) {
          // Copy selectedItem into editedItem whenever it changes
          if (newVal && Object.keys(newVal).length > 0) {
            this.editedItem = { ...newVal };
          }
        },
        deep: true,
        immediate: true,
      },
    },
    mounted() {
      nextTick(() => {
        // Initialize our modal once the component is mounted
        this.modalInstance = new Modal(this.$refs.editModal, {
          backdrop: "static",
        });
      });
    },
    methods: {
      validateAndUpdateItem() {
        if (
          !this.editedItem.product_name ||
          !this.editedItem.description ||
          this.editedItem.price <= 0
        ) {
          alert("Please fill all required fields correctly.");
          return;
        }
        this.updateItem();
      },
      async updateItem() {
        if (!this.editedItem.id) {
          console.error("Error: editedItem ID is missing.");
          return;
        }
        try {
          const response = await fetch(
            `http://127.0.0.1:8000/api/items/${this.editedItem.id}/`,
            {
              method: "PUT",
              headers: { "Content-Type": "application/json" },
              body: JSON.stringify(this.editedItem),
            }
          );
  
          if (!response.ok) {
            const errorData = await response.json();
            console.error("Failed to update item:", errorData);
            return;
          }
  
          console.log("Item updated successfully!");
          // Let parent know we updated an item
          this.$emit("item-updated", this.editedItem.id);
  
          // Hide the modal
          const modalElement = this.$refs.editModal;
          const modal = Modal.getInstance(modalElement);
          if (modal) {
            modal.hide();
          }
        } catch (error) {
          console.error("Update error:", error);
        }
      },
    },
  };
  </script>
  
  <style>
  .modal-content {
    background-color: #f8f9fa;
    border-radius: 10px;
  }
  </style>
  