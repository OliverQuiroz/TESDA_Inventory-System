<template>
  <div class="modal fade" id="editItemModal" tabindex="-1" ref="editModal">
    <div class="modal-dialog">
      <div class="modal-content p-4">
        <div class="modal-header border-0 text-center d-flex flex-column w-100">
          <h5 class="modal-title fw-bold text-center w-100">EDIT ITEM</h5>
          <button type="button" class="btn-close position-absolute end-0 me-3" data-bs-dismiss="modal"></button>
        </div>

        <div class="modal-body">
          <form @submit.prevent="validateAndUpdateItem">
            <div class="mb-3">
              <label>Product Name</label>
              <input type="text" class="form-control" v-model.trim="editedItem.product_name" required />
            </div>

            <div class="mb-3">
              <label>Description</label>
              <textarea class="form-control" v-model.trim="editedItem.description" required></textarea>
            </div>

            <div class="mb-3">
              <label>Price</label>
              <input type="number" class="form-control" v-model="editedItem.price" min="1" required />
            </div>

            <div class="mb-3">
              <label>Date of Purchase</label>
              <input type="date" class="form-control" v-model="editedItem.date_of_purchase" required />
            </div>

            <div class="mb-3">
              <label>Transfer to</label>
              <input
                type="text"
                class="form-control"
                v-model.trim="transferRecipientTemp"
                :disabled="!transferEditMode"
                placeholder="Enter new recipient"
              />
              <div class="mt-2">
                <button
                  v-if="!transferEditMode"
                  @click="enableTransferEdit"
                  type="button"
                  class="btn btn-sm btn-outline-primary"
                >
                  Transfer Owner
                </button>
                <button
                  v-if="transferEditMode"
                  @click="cancelTransfer"
                  type="button"
                  class="btn btn-sm btn-outline-secondary ms-2"
                >
                  Cancel
                </button>
              </div>
            </div>

            <div class="mb-3">
              <label>Classification</label>
              <select class="form-control" v-model="editedItem.classification" required>
                <option value="PPE">PPE</option>
                <option value="SE">SE</option>
              </select>
            </div>

            <div class="mb-3">
              <label class="fw-bold">Recipient History</label>
              <ul class="list-group" v-if="uniqueRecipientHistory.length">
                <li
                  v-for="(entry, index) in uniqueRecipientHistory"
                  :key="index"
                  class="list-group-item d-flex justify-content-between align-items-center"
                >
                  {{ entry.name }}
                  <span class="badge bg-secondary">{{ entry.date }}</span>
                </li>
              </ul>
              <div v-else>
                <small class="text-muted">No transfer history</small>
              </div>
            </div>

            <div class="modal-footer">
              <button type="submit" class="btn btn-success" :disabled="!isChanged">
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
    originalItem: {},
    modalInstance: null,
    transferEditMode: false,
    transferRecipientTemp: "", // hold newly typed recipient
    };
  },
  computed: {
    uniqueRecipientHistory() {
      const seen = new Set();
      return (this.editedItem.recipient_history || []).filter(entry => {
        const key = `${entry.name}-${entry.date}`;
        if (seen.has(key)) return false;
        seen.add(key);
        return true;
      });
    },
    isChanged() {
      const fields = [
        "product_name",
        "description",
        "price",
        "date_of_purchase",
        "classification",
      ];

      const hasBaseChanges = fields.some(
        field => this.editedItem[field] !== this.originalItem[field]
      );

      const hasRecipientChanged =
        this.transferEditMode && this.transferRecipientTemp.trim() !== "";

      return hasBaseChanges || hasRecipientChanged;
    },
  },
  watch: {
  selectedItem: {
    handler(newVal) {
      if (newVal && Object.keys(newVal).length > 0) {
        this.originalItem = JSON.parse(JSON.stringify(newVal));
        this.editedItem = JSON.parse(JSON.stringify(newVal));
        this.transferEditMode = false;
        this.transferRecipientTemp = "";
      }
    },
    deep: true,
    immediate: true,
    },
  },
  mounted() {
    nextTick(() => {
      this.modalInstance = new Modal(this.$refs.editModal, {
        backdrop: "static",
      });
    });
  },
  methods: {
    enableTransferEdit() {
        this.transferEditMode = true;
        this.transferRecipientTemp = ""; // always start empty
      },

      cancelTransfer() {
        this.transferRecipientTemp = "";
        this.transferEditMode = false;
      },

      validateAndUpdateItem() {
        if (
          !this.editedItem.product_name ||
          !this.editedItem.description ||
          this.editedItem.price <= 0
        ) {
          alert("Please fill all required fields correctly.");
          return;
        }

        // Apply transfer recipient if transfer is enabled
        if (this.transferEditMode && this.transferRecipientTemp.trim()) {
          this.editedItem.recipient = this.transferRecipientTemp.trim();
        }

        this.updateItem();
      },

      applyTransferRecipient() {
        if (this.transferRecipientTemp.trim()) {
          this.editedItem.recipient = this.transferRecipientTemp.trim();
        }
    },

    async updateItem() {
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

        this.$emit("item-updated", this.editedItem.id);
        const modal = Modal.getInstance(this.$refs.editModal);
        if (modal) modal.hide();
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
