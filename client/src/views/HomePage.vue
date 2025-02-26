<template>
  <div class="container mt-4">
    <div class="row mb-4">
      <!-- Total Registered Items -->
      <div class="col-md-4">
        <div class="card text-center p-3 filter-card" @click="filterBy('all')">
          <h4>{{ items.length }}</h4>
          <p>Total Registered Items</p>
        </div>
      </div>

      <div class="col-md-4">
        <div class="card text-center p-3 filter-card" @click="filterBy('SE')">
          <h4>{{ seCount }}</h4>
          <p>(SE) Semi-Expendable</p>
        </div>
      </div>

      <div class="col-md-4">
        <div class="card text-center p-3 filter-card" @click="filterBy('PPE')">
          <h4>{{ ppeCount }}</h4>
          <p>(PPE) Property-Plant & Equipment</p>
        </div>
      </div>

    </div>

    <!-- Search box -->
    <div class="d-flex justify-content-center mb-3">
      <input
        v-model="searchQuery"
        type="text"
        class="form-control w-50 text-center"
        placeholder="Search"
      />
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
        <tr
          v-for="(item, index) in paginatedItems"
          :key="index"
          @click="openModal(item)"
          class="clickable-row"
        >
          <td>{{ item.inventory_number }}</td>
          <td>{{ item.product_name }}</td>
          <td>{{ item.description }}</td>
          <!-- Convert price to float before .toFixed() -->
          <td>₱ {{ parseFloat(item.price || 0).toFixed(2) }}</td>
          <td>{{ item.date_of_purchase }}</td>
          <td>{{ item.recipient }}</td>
          <td>{{ item.classification }}</td>
          <td>
            <img
              v-if="item.qr_code"
              :src="item.qr_code"
              alt="QR Code"
              width="50"
              height="50"
            />
          </td>
        </tr>
      </tbody>
    </table>

    <!-- Pagination Controls -->
    <div class="d-flex justify-content-between align-items-center mt-3">
      <nav>
        <ul class="pagination">
          <li class="page-item" :class="{ disabled: currentPage === 1 }">
            <button class="page-link" @click="changePage(currentPage - 1)">
              &larr; Previous
            </button>
          </li>
          <li
            v-for="page in totalPages"
            :key="page"
            class="page-item"
            :class="{ active: page === currentPage }"
          >
            <button class="page-link" @click="changePage(page)">
              {{ page }}
            </button>
          </li>
          <li
            class="page-item"
            :class="{ disabled: currentPage === totalPages }"
          >
            <button class="page-link" @click="changePage(currentPage + 1)">
              Next &rarr;
            </button>
          </li>
        </ul>
      </nav>

      <!-- Button to Open Add Item Modal -->
      <button
        class="btn btn-primary"
        data-bs-toggle="modal"
        data-bs-target="#addItemModal"
      >
        Add Item
      </button>
    </div>

    <!-- Include the Add Item Modal -->
    <!-- Listen for 'item-added' so we can refresh the list -->
    <AddItemModal @item-added="fetchItems" />

    <!-- Modal for Item Details -->
    <div
      class="modal fade"
      id="itemModal"
      tabindex="-1"
      aria-labelledby="itemModalLabel"
      aria-hidden="true"
    >
      <div class="modal-dialog">
        <div class="modal-content">
          <div class="modal-header">
            <h5 class="modal-title">Item Details</h5>
            <button
              type="button"
              class="btn-close"
              data-bs-dismiss="modal"
              aria-label="Close"
            ></button>
          </div>
          <div class="modal-body">
            <p>
              <strong>Inventory Number:</strong>
              {{ selectedItem?.inventory_number }}
            </p>
            <p>
              <strong>Product Name:</strong>
              {{ selectedItem?.product_name }}
            </p>
            <p>
              <strong>Description:</strong>
              {{ selectedItem?.description }}
            </p>
            <p>
              <strong>Price:</strong>
              ₱ {{ parseFloat(selectedItem?.price || 0).toFixed(2) }}
            </p>
            <p>
              <strong>Date of Purchase:</strong>
              {{ selectedItem?.date_of_purchase }}
            </p>
            <p>
              <strong>Recipient:</strong>
              {{ selectedItem?.recipient }}
            </p>
            <p>
              <strong>Classification:</strong>
              {{ selectedItem?.classification }}
            </p>
            <p><strong>QR Code:</strong></p>
            <img
              v-if="selectedItem?.qr_code"
              :src="selectedItem.qr_code"
              alt="QR Code"
              width="100"
              height="100"
            />
          </div>
          <div class="modal-footer">
            <button
              type="button"
              class="btn btn-info"
              data-bs-dismiss="modal"
            >
              Edit
            </button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import AddItemModal from "@/components/AddItem.vue";
import { Modal } from "bootstrap";

export default {
  name: "HomePage",
  components: {
    AddItemModal,
  },
  data() {
    return {
      items: [],
      currentPage: 1,
      itemsPerPage: 5,
      searchQuery: "",
      selectedFilter: "all",
      selectedItem: null,
    };
  },
  computed: {
    filteredItems() {
      return this.items
        .filter((item) => this.selectedFilter === "all" || item.classification === this.selectedFilter)
        .filter((item) => {
          const query = this.searchQuery.toLowerCase();
          return (
            item.product_name.toLowerCase().includes(query) ||
            item.inventory_number.toLowerCase().includes(query) ||
            item.recipient.toLowerCase().includes(query) ||
            item.classification.toLowerCase().includes(query)
          );
        });
    },
    totalPages() {
      return Math.ceil(this.filteredItems.length / this.itemsPerPage);
    },
    paginatedItems() {
      const start = (this.currentPage - 1) * this.itemsPerPage;
      return this.filteredItems.slice(start, start + this.itemsPerPage);
    },
    seCount() {
      return this.items.filter((item) => item.classification === "SE").length;
    },
    ppeCount() {
      return this.items.filter((item) => item.classification === "PPE").length;
    },
  },
  methods: {
    async fetchItems() {
      try {
        const response = await fetch("http://127.0.0.1:8000/api/items/");
        if (!response.ok) {
          throw new Error("Failed to fetch items");
        }
        this.items = await response.json();
      } catch (error) {
        console.error("fetchItems error:", error);
      }
    },
    filterBy(type) {
      if (type === "SE" || type === "PPE" || type === "all") {
        this.selectedFilter = type;
        this.currentPage = 1;
      }
    },
    openModal(item) {
      this.selectedItem = item;
      const modalElement = document.getElementById("itemModal");
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
    // fetch existing items from the backend on mount
    await this.fetchItems();
  },
};
</script>

<style>
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
