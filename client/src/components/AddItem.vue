<template>
  <div>
    <!-- ADD ITEM MODAL -->
    <div class="modal fade" id="addItemModal" tabindex="-1">
      <div class="modal-dialog modal-dialog-centered modal-xl">
        <div class="modal-content p-4">
          <div class="modal-header border-0 d-flex flex-column w-100">
            <h5 class="modal-title fw-bold w-100 text-center">ADD ITEM</h5>
            <button
              type="button"
              class="btn-close position-absolute end-0 me-3"
              data-bs-dismiss="modal"
            ></button>
          </div>

          <div class="modal-body">
            <form @submit.prevent="addItem">
              <div class="row gx-4 gy-3">
                <!-- Row 1 -->
                <div class="col-lg-4 col-md-6">
                  <div class="form-floating">
                    <input v-model="acquisitionDate" type="date" class="form-control" required />
                    <label>Date of Acquisition</label>
                  </div>
                </div>
                <div class="col-lg-4 col-md-6">
                  <div class="form-floating">
                    <input v-model="accountablePerson" type="text" class="form-control" placeholder="Accountable Person" required />
                    <label>Accountable Person</label>
                  </div>
                </div>
                <div class="col-lg-4 col-md-6">
                  <div class="form-floating">
                    <input v-model="fund" type="text" class="form-control" placeholder="Fund" />
                    <label>Fund</label>
                  </div>
                </div>

                <!-- Row 2 -->
                <div class="col-lg-6">
                  <div class="form-floating">
                    <input v-model="article" type="text" class="form-control" placeholder="Article" required />
                    <label>Article</label>
                  </div>
                </div>
                <div class="col-lg-6">
                  <div class="form-floating">
                    <input v-model="description" type="text" class="form-control" placeholder="Description" />
                    <label>Description</label>
                  </div>
                </div>

                <!-- Row 3 -->
                <div class="col-lg-4">
                  <div class="form-floating">
                    <input v-model="uacsCode" type="text" class="form-control" placeholder="UACS Code" />
                    <label>UACS Code</label>
                  </div>
                </div>
                <div class="col-lg-4">
                  <div class="form-floating">
                    <select v-model="uacsCategory" class="form-select">
                      <option value="SE">Semi-Expendable</option>
                      <option value="PPE">Property, Plant & Equipment</option>
                    </select>
                    <label>Category for UACS Code</label>
                  </div>
                </div>
                <div class="col-lg-4">
                  <div class="form-floating">
                    <input v-model.number="unitCost" type="number" step="0.01" class="form-control" placeholder="Unit Cost" />
                    <label>Unit Cost</label>
                  </div>
                </div>

                <!-- Row 4 -->
                <div class="col-lg-4">
                  <div class="form-floating">
                    <input v-model.number="quantity" type="number" min="1" class="form-control" placeholder="Quantity" />
                    <label>Quantity</label>
                  </div>
                </div>
                <div class="col-lg-4">
                  <div class="form-floating">
                    <input :value="totalCost" class="form-control" disabled />
                    <label>Total Cost</label>
                  </div>
                </div>
                <div class="col-lg-4">
                  <div class="form-floating">
                    <input v-model="unit" type="text" class="form-control" placeholder="Unit" />
                    <label>Unit</label>
                  </div>
                </div>

                <!-- Row 5 -->
                <div class="col-lg-6">
                  <div class="form-floating">
                    <input v-model="location" type="text" class="form-control" placeholder="Location" />
                    <label>Location</label>
                  </div>
                </div>
                <div class="col-lg-6">
                  <div class="form-floating">
                    <input v-model="propertyNumber" type="text" class="form-control" placeholder="Property Number" required />
                    <label>Property Number</label>
                  </div>
                </div>

                <!-- Row 6 -->
                <div class="col-lg-4">
                  <div class="form-floating">
                    <input v-model="icsNumber" type="text" class="form-control" placeholder="ICS No." />
                    <label>ICS No.</label>
                  </div>
                </div>
                <div class="col-lg-4">
                  <div class="form-floating">
                    <input v-model="poDate" type="date" class="form-control" />
                    <label>Date of PO</label>
                  </div>
                </div>
                <div class="col-lg-4">
                  <div class="form-floating">
                    <input v-model="poNumber" type="text" class="form-control" placeholder="PO #" />
                    <label>PO #</label>
                  </div>
                </div>

                <!-- Row 7 -->
                <div class="col-12">
                  <div class="form-floating">
                    <input v-model="supplierName" type="text" class="form-control" placeholder="Supplier Name" />
                    <label>Supplier Name</label>
                  </div>
                </div>
              </div>

              <!-- Button -->
              <div class="text-center mt-4">
                <button type="submit" class="btn btn-success px-5">Add Item</button>
              </div>
            </form>
          </div>
        </div>
      </div>
    </div>

    <!-- SUCCESS MODAL -->
<div class="modal fade" id="addItemSuccessModal" tabindex="-1">
  <div class="modal-dialog modal-dialog-centered">
    <div class="modal-content text-center p-4 rounded-4 shadow-sm">
      <div class="mb-3">
        <i class="bi bi-check-circle-fill text-success fs-1"></i>
      </div>
      <h5 class="fw-bold mb-1">Item Successfully Added!</h5>
      <p class="text-muted small mb-3">Your item has been saved to the inventory.</p>

      <div v-if="qrImage" class="mb-3">
        <img :src="qrImage" alt="QR Code" class="img-fluid border p-1" style="max-width: 180px;" />
        <p class="mb-1 mt-2 fw-semibold">{{ article }}</p>
        <p class="text-muted small">{{ propertyNumber }}</p>
      </div>

      <div class="d-flex justify-content-center gap-2 mt-2">
        <button class="btn btn-primary btn-sm px-4" data-bs-dismiss="modal">
          OK
        </button>
      </div>
    </div>
  </div>
</div>


    <!-- hidden canvas for QR rendering -->
    <canvas ref="qrCanvas" style="display: none"></canvas>
  </div>
</template>

<script>
import { ref, computed, onMounted } from "vue";
import { Modal } from "bootstrap";

export default {
  name: "AddItemModal",
  emits: ["item-added"],
  setup(_, { emit }) {
    const acquisitionDate = ref("");
    const accountablePerson = ref("");
    const fund = ref("");
    const article = ref("");
    const description = ref("");
    const uacsCode = ref("");
    const uacsCategory = ref("SE");
    const unitCost = ref(0);
    const quantity = ref(1);
    const unit = ref("");
    const location = ref("");
    const propertyNumber = ref("");
    const icsNumber = ref("");
    const poDate = ref("");
    const poNumber = ref("");
    const supplierName = ref("");

    const totalCost = computed(
      () => (unitCost.value || 0) * (quantity.value || 0)
    );

    const resetForm = () => {
      acquisitionDate.value = "";
      accountablePerson.value = "";
      fund.value = "";
      article.value = "";
      description.value = "";
      uacsCode.value = "";
      uacsCategory.value = "SE";
      unitCost.value = 0;
      quantity.value = 1;
      unit.value = "";
      location.value = "";
      propertyNumber.value = "";
      icsNumber.value = "";
      poDate.value = "";
      poNumber.value = "";
      supplierName.value = "";
    };

    const addItem = async () => {
      if (!propertyNumber.value) {
        alert("Property number is required.");
        return;
      }

      const existing = await fetch("http://127.0.0.1:8000/api/items/");
      if ((await existing.json()).some((i) => i.property_number === propertyNumber.value)) {
        alert("Item with this Property Number already exists.");
        return;
      }

      const payload = {
        date_of_acquisition: acquisitionDate.value || null,
        accountable_person: accountablePerson.value,
        fund: fund.value,
        article: article.value,
        description: description.value,
        uacs_code: uacsCode.value,
        uacs_category: uacsCategory.value,
        unit_cost: unitCost.value,
        quantity: quantity.value,
        total_cost: totalCost.value,
        unit: unit.value,
        location: location.value,
        property_number: propertyNumber.value,
        ics_number: icsNumber.value,
        date_of_po: poDate.value || null,
        po_number: poNumber.value,
        supplier_name: supplierName.value,
      };

      const res = await fetch("http://127.0.0.1:8000/api/items/", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(payload),
      });

      const data = await res.json();
      if (!res.ok) {
        alert(JSON.stringify(data));
        return;
      }

      Modal.getInstance(document.getElementById("addItemModal")).hide();
      new Modal(document.getElementById("addItemSuccessModal")).show();

      emit("item-added");
      resetForm();
    };

    onMounted(() => {
      document
        .getElementById("addItemSuccessModal")
        .addEventListener("hidden.bs.modal", () => {
          // Optional cleanup
        });
    });

    return {
      acquisitionDate,
      accountablePerson,
      fund,
      article,
      description,
      uacsCode,
      uacsCategory,
      unitCost,
      quantity,
      totalCost,
      unit,
      location,
      propertyNumber,
      icsNumber,
      poDate,
      poNumber,
      supplierName,
      addItem,
    };
  },
};
</script>
