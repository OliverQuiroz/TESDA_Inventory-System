<template>
  <div>
    <!-- Modal -->
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
                <input type="text" v-model="inventoryNumber" class="form-control" placeholder="Enter Inventory Number">
                <label>Enter Inventory Number</label>
              </div>

              <div class="form-floating mb-3">
                <input type="text" v-model="productName" class="form-control" placeholder="Enter Product Name">
                <label>Enter Product Name</label>
              </div>

              <div class="form-floating mb-3">
                <input type="text" v-model="description" class="form-control" placeholder="Enter Description">
                <label>Enter Description</label>
              </div>

              <div class="form-floating mb-3">
                <input type="number" v-model="price" class="form-control" placeholder="Enter Price">
                <label>Enter Price</label>
              </div>

              <div class="form-floating mb-3">
                <input type="date" v-model="purchaseDate" class="form-control" placeholder="Date of Purchase">
                <label>Date of Purchase</label>
              </div>

              <div class="form-floating mb-3">
                <input type="text" v-model="recipient" class="form-control" placeholder="Enter Recipient">
                <label>Enter Recipient</label>
              </div>

              <div class="form-floating mb-3">
                <select v-model="classification" class="form-select">
                  <option value="semi-expendable">Semi-expendable</option>
                  <option value="ppe">PPE</option>
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
  </div>
</template>

<script>
import { ref } from "vue";

export default {
  setup() {
    const inventoryNumber = ref("");
    const productName = ref("");
    const description = ref("");
    const price = ref("");
    const purchaseDate = ref("");
    const recipient = ref("");
    const classification = ref("");

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
    };

    return { inventoryNumber, productName, description, price, purchaseDate, recipient, classification, addItem };
  },
};
</script>

<style scoped>
.modal-content {
  background-color: #f8f9fa;
  border-radius: 10px;
}

/* Adjust floating labels */
.form-floating label {
  color: #6c757d;
  font-size: 14px;
}

.form-floating input,
.form-floating select {
  padding-top: 1rem;
  padding-bottom: 1rem;
}

</style>
