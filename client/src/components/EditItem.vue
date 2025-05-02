<template>
  <!-- EDIT ITEM MODAL -->
  <div class="modal fade" id="editItemModal" tabindex="-1" ref="editModal">
    <div class="modal-dialog modal-dialog-centered modal-xl">
      <div class="modal-content p-4">
        <div class="modal-header border-0 d-flex flex-column w-100 text-center">
          <h5 class="modal-title fw-bold w-100">EDIT ITEM</h5>
          <button class="btn-close position-absolute end-0 me-3" data-bs-dismiss="modal"></button>
        </div>

        <div class="modal-body">
          <form @submit.prevent="validateAndSave">
            <div class="row g-3">
              <!-- ROW 1 -->
              <div class="col-md-4">
                <div class="form-floating">
                  <input type="date" v-model="edited.date_of_acquisition" class="form-control" />
                  <label>Date of Acquisition</label>
                </div>
              </div>

              <!-- Accountable Person w/ button on the right -->
              <div class="col-md-4">
                <div class="form-floating position-relative">
                  <input
                    v-model="edited.accountable_person"
                    :disabled="transferDisabled"
                    class="form-control pe-7"
                    id="accountableInput"
                    placeholder="Accountable Person"
                  />
                  <label for="accountableInput">Accountable Person</label>
                  <button
                    type="button"
                    class="btn btn-outline-primary btn-sm position-absolute top-50 end-0 translate-middle-y me-2"
                    @click="toggleTransfer"
                    style="z-index: 10; height: 28px; font-size: 12px; padding: 0 8px;"
                  >
                    {{ transferButtonLabel }}
                  </button>
                </div>
              </div>

              <div class="col-md-4">
                <div class="form-floating">
                  <input v-model="edited.fund" class="form-control" placeholder="Fund" />
                  <label>Fund</label>
                </div>
              </div>

              <!-- The rest of your form continues as is... -->
              <!-- ROW 2 -->
              <div class="col-md-4">
                <div class="form-floating">
                  <input v-model="edited.article" class="form-control" placeholder="Article" />
                  <label>Article</label>
                </div>
              </div>
              <div class="col-md-8">
                <div class="form-floating">
                  <input v-model="edited.description" class="form-control" placeholder="Description" />
                  <label>Description</label>
                </div>
              </div>

              <!-- ROW 3 -->
              <div class="col-md-4">
                <div class="form-floating">
                  <input v-model="edited.uacs_code" class="form-control" placeholder="UACS Code" />
                  <label>UACS Code</label>
                </div>
              </div>
              <div class="col-md-4">
                <div class="form-floating">
                  <select v-model="edited.uacs_category" class="form-select">
                    <option value="SE">SE (Semi-Expendable)</option>
                    <option value="PPE">PPE (Property, Plant & Equipment)</option>
                  </select>
                  <label>Category for UACS</label>
                </div>
              </div>
              <div class="col-md-4">
                <div class="form-floating">
                  <input
                    type="number"
                    min="0"
                    step="0.01"
                    v-model.number="edited.unit_cost"
                    class="form-control"
                    placeholder="Unit Cost"
                  />
                  <label>Unit Cost</label>
                </div>
              </div>

              <!-- ROW 4 -->
              <div class="col-md-4">
                <div class="form-floating">
                  <input
                    type="number"
                    min="1"
                    v-model.number="edited.quantity"
                    class="form-control"
                    placeholder="Quantity"
                  />
                  <label>Quantity</label>
                </div>
              </div>
              <div class="col-md-4">
                <div class="form-floating">
                  <input :value="totalCost" class="form-control" disabled />
                  <label>Total Cost</label>
                </div>
              </div>
              <div class="col-md-4">
                <div class="form-floating">
                  <input v-model="edited.unit" class="form-control" placeholder="Unit" />
                  <label>Unit</label>
                </div>
              </div>

              <!-- ROW 5 -->
              <div class="col-md-4">
                <div class="form-floating">
                  <input v-model="edited.location" class="form-control" placeholder="Location" />
                  <label>Location</label>
                </div>
              </div>
              <div class="col-md-4">
                <div class="form-floating">
                  <input v-model="edited.property_number" class="form-control" placeholder="Property Number" />
                  <label>Property Number</label>
                </div>
              </div>
              <div class="col-md-4">
                <div class="form-floating">
                  <input v-model="edited.ics_number" class="form-control" placeholder="ICS No." />
                  <label>ICS No.</label>
                </div>
              </div>

              <!-- ROW 6 -->
              <div class="col-md-4">
                <div class="form-floating">
                  <input type="date" v-model="edited.date_of_po" class="form-control" />
                  <label>Date of PO</label>
                </div>
              </div>
              <div class="col-md-4">
                <div class="form-floating">
                  <input v-model="edited.po_number" class="form-control" placeholder="PO #" />
                  <label>PO #</label>
                </div>
              </div>
              <div class="col-md-4">
                <div class="form-floating">
                  <input v-model="edited.supplier_name" class="form-control" placeholder="Supplier Name" />
                  <label>Supplier Name</label>
                </div>
              </div>
            </div>

            <!-- Save Button -->
            <div class="text-center mt-4">
              <button class="btn btn-success px-4 py-2 fs-6 rounded" type="submit" :disabled="!isChanged">
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
  name: "EditItem",
  props: ["selectedItem"],
  emits: ["item-updated"],

  data() {
    return {
      edited: {},
      original: {},
      transferDisabled: true,
      transferButtonLabel: "Transfer Owner",
      originalAccountablePerson: "",
    };
  },

  computed: {
    totalCost() {
      return (
        (parseFloat(this.edited.unit_cost) || 0) *
        (parseInt(this.edited.quantity) || 0)
      ).toLocaleString("en-US", { minimumFractionDigits: 2 });
    },
    isChanged() {
      return JSON.stringify(this.edited) !== JSON.stringify(this.original);
    },
  },

  watch: {
    selectedItem: {
      deep: true,
      immediate: true,
      handler(val) {
        if (val && Object.keys(val).length) {
          this.original = JSON.parse(JSON.stringify(val));
          this.edited = JSON.parse(JSON.stringify(val));
          this.transferDisabled = true;
          this.transferButtonLabel = "Transfer Owner";
          this.originalAccountablePerson = val.accountable_person;
        }
      },
    },
  },

  mounted() {
    nextTick(() => new Modal(this.$refs.editModal, { backdrop: "static" }));
  },

  methods: {
    toggleTransfer() {
      if (this.transferDisabled) {
        this.transferDisabled = false;
        this.transferButtonLabel = "Cancel";
      } else {
        this.transferDisabled = true;
        this.transferButtonLabel = "Transfer Owner";
        this.edited.accountable_person = this.originalAccountablePerson;
      }
    },

    validateAndSave() {
      if (!this.edited.article || !this.edited.description) {
        alert("Article & Description are required.");
        return;
      }
      this.edited.total_cost =
        (parseFloat(this.edited.unit_cost) || 0) *
        (parseInt(this.edited.quantity) || 0);

      this.saveItem();
    },

    async saveItem() {
      try {
        const res = await fetch(
          `http://127.0.0.1:8000/api/items/${this.edited.id}/`,
          {
            method: "PUT",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify(this.edited),
          }
        );
        if (!res.ok) throw new Error("Update failed");
        this.$emit("item-updated", this.edited.id);
        Modal.getInstance(this.$refs.editModal).hide();
      } catch (e) {
        console.error(e);
        alert("Failed to update item.");
      }
    },
  },
};
</script>

<style scoped>
.modal-content {
  background: #f8f9fa;
  border-radius: 10px;
}
</style>
