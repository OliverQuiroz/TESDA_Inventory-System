<template>
  <div class="container mt-4">
    <div class="row mb-4">
      <!-- Total Registered Items -->
      <div class="col-md-4">
        <div class="card text-center p-3 filter-card" @click="filterBy('all')">
          <i class="bi bi-box-se"></i>
          <h4>{{ items.length }}</h4>
          <p>Total Registered Items</p>
        </div>
      </div>
      <!-- SE (Semi-Expendable) -->
      <div class="col-md-4">
        <div class="card text-center p-3 filter-card" @click="filterBy('SE')">
          <i class="bi bi-clipboard"></i>
          <h4>{{ seCount }}</h4>
          <p>(SE) Semi-Expendable</p>
        </div>
      </div>
      <!-- PPE (Property, Plant & Equipment) -->
      <div class="col-md-4">
        <div class="card text-center p-3 filter-card" @click="filterBy('PPE')">
          <i class="bi bi-clipboard"></i>
          <h4>{{ ppeCount }}</h4>
          <p>(PPE) Property-Plant & Equipment</p>
        </div>
      </div>
    </div>

    <div class="d-flex justify-content-between mb-3">
      <input v-model="searchQuery" type="text" class="form-control w-25" placeholder="Search by Name, Inventory No, Recipient, Classification" />
    </div>

    <table class="table table-bordered text-center">
      <thead>
        <tr>
          <th>Inventory Number</th>
          <th>Product Name</th>
          <th>Description</th>
          <th>Price</th>
          <th>Date of Purchase</th>
          <th>Memorandum of Receipt (MR)</th>
          <th>Classification</th>
          <th>QR Code</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="(item, index) in paginatedItems" :key="index" @click="openModal(item)" class="clickable-row">
          <td>{{ item.inventoryNumber }}</td>
          <td>{{ item.productName }}</td>
          <td>{{ item.description }}</td>
          <td>${{ item.price?.toFixed(2) || '0.00' }}</td>
          <td>{{ item.dateOfPurchase }}</td>
          <td>{{ item.recipient }}</td>
          <td>{{ item.classification }}</td>
          <td>
            <img :src="item.qrCode" alt="QR Code" width="50" height="50" />
          </td>
        </tr>
      </tbody>
    </table>

    <!-- Pagination Controls -->
    <div class="d-flex justify-content-between align-items-center mt-3">
      <nav>
        <ul class="pagination">
          <li class="page-item" :class="{ disabled: currentPage === 1 }">
            <button class="page-link" @click="changePage(currentPage - 1)">&larr; Previous</button>
          </li>
          <li v-for="page in totalPages" :key="page" class="page-item" :class="{ active: page === currentPage }">
            <button class="page-link" @click="changePage(page)">{{ page }}</button>
          </li>
          <li class="page-item" :class="{ disabled: currentPage === totalPages }">
            <button class="page-link" @click="changePage(currentPage + 1)">Next &rarr;</button>
          </li>
        </ul>
      </nav>
        <!-- Button to Open Add Item Modal -->
        <button class="btn btn-primary" data-bs-toggle="modal" data-bs-target="#addItemModal">
          Add Item
        </button>
      </div>

      <!-- Include the Add Item Modal -->
      <AddItem />

    <!-- Modal for Item Details -->
    <div class="modal fade" id="itemModal" tabindex="-1" aria-labelledby="itemModalLabel" aria-hidden="true">
      <div class="modal-dialog">
        <div class="modal-content">
          <div class="modal-header">
            <h5 class="modal-title">Item Details</h5>
            <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
          </div>
          <div class="modal-body">
            <p><strong>Inventory Number:</strong> {{ selectedItem?.inventoryNumber }}</p>
            <p><strong>Product Name:</strong> {{ selectedItem?.productName }}</p>
            <p><strong>Description:</strong> {{ selectedItem?.description }}</p>
            <p><strong>Price:</strong> ${{ selectedItem?.price?.toFixed(2) || '0.00' }}</p>
            <p><strong>Date of Purchase:</strong> {{ selectedItem?.dateOfPurchase }}</p>
            <p><strong>Recipient:</strong> {{ selectedItem?.recipient }}</p>
            <p><strong>Classification:</strong> {{ selectedItem?.classification }}</p>
            <p><strong>QR Code:</strong></p>
            <img :src="selectedItem?.qrCode" alt="QR Code" width="100" height="100" />
          </div>
          <div class="modal-footer">
            <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Close</button>
          </div>
        </div>
      </div>
    </div>

  </div>
</template>

<script>
import AddItem from '../components/AddItem.vue';

import QRCode from "qrcode";
import { Modal } from 'bootstrap';

export default {
  name: "InventoryPage",
  components:{
    AddItem,
  },
  data() {
    return {
      items: [],
      filteredItems: [],
      currentPage: 1,
      itemsPerPage: 5,
      searchQuery: "",
      selectedFilter: "all",
      selectedItem: null
    };
  },
  computed: {
    totalPages() {
      return Math.ceil(this.filteredItems.length / this.itemsPerPage);
    },
    paginatedItems() {
      const start = (this.currentPage - 1) * this.itemsPerPage;
      return this.filteredItems.slice(start, start + this.itemsPerPage);
    },
    seCount() {
      return this.items.filter(item => item.classification === 'SE').length;
    },
    ppeCount() {
      return this.items.filter(item => item.classification === 'PPE').length;
    }
  },
  methods: {
    async generateQRCode(text) {
      try {
        return await QRCode.toDataURL(text);
      } catch (error) {
        console.error("QR Code generation error:", error);
        return "";
      }
    },
    async generateDummyData() {
      const data = Array.from({ length: 50 }, async (_, i) => ({
        inventoryNumber: `INV-${i + 1}`,
        productName: `Product ${i + 1}`,
        description: `Description of product ${i + 1}`,
        price: (i + 1) * 10 || 0,
        dateOfPurchase: `2024-02-${(i % 28) + 1}`,
        recipient: `Recipient ${i + 1}`,
        classification: i % 2 === 0 ? "SE" : "PPE",
        qrCode: await this.generateQRCode(`INV-${i + 1}`),
      }));

      Promise.all(data).then((resolvedData) => {
        this.items = resolvedData;
        this.filteredItems = resolvedData;
      });
    },
    filterBy(type) {
      this.selectedFilter = type;
      this.filteredItems = type === "all" ? this.items : this.items.filter(item => item.classification === type);
      this.currentPage = 1;
    },
    openModal(item) {
      this.selectedItem = item;
      const modalElement = document.getElementById('itemModal');
      const modal = new Modal(modalElement);
      modal.show();
    },
    changePage(page) {
      if (page >= 1 && page <= this.totalPages) {
        this.currentPage = page;
      }
    },
  },
  async mounted() {
    await this.generateDummyData();
  },
};
</script>

<style scoped>
.clickable-row {
  cursor: pointer;
}

.filter-card {
  cursor: pointer;
  transition: 0.3s;
}

.filter-card:hover {
  background-color: #f8f9fa;
  transform: scale(1.05);
}
</style>
