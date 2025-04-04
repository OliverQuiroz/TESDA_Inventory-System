<template>
  <div class="container-fluid mt-4 px-5">
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

    <!-- Items Table with fixed height -->
    <div class="table-wrapper">
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
            <th>Actions</th>
          </tr>
        </thead>
        <tbody>
          <tr
            v-for="(item, index) in paginatedItems"
            :key="index"
            @click="openModal(item)"
            class="clickable-row"
            :class="{ 'table-success animate-highlight': item.id === updatedItemId }"
          >
            <td>{{ item.inventory_number }}</td>
            <td>{{ item.product_name }}</td>
            <td>{{ truncateText(item.description, 30) }}</td>
            <td>₱ {{ formatPrice(item.price) }}</td>
            <td>{{ item.date_of_purchase }}</td>
            <td>{{ item.recipient }}</td>
            <td>{{ item.classification }}</td>
            <td>
              <img
                v-if="item.qr_code"
                :src="getFullImageUrl(item.qr_code)"
                alt="QR Code"
                width="50"
                height="50"
              />
            </td>
            <td>
              <button
                class="btn btn-sm btn-outline-info me-1"
                @click.stop="openEditModalFromTable(item)"
                title="Edit"
              >
                <i class="bi bi-pencil-square"></i>
              </button>
              <button
                class="btn btn-sm btn-outline-danger"
                @click.stop="deleteItem(item.id)"
                title="Delete"
              >
                <i class="bi bi-trash"></i>
              </button>
            </td>
          </tr>
        </tbody>
      </table>
    </div>

    <!-- Pagination + Add Item -->
    <div class="d-flex justify-content-between align-items-center mt-3 pagination-footer">
      <nav>
        <ul class="pagination">
          <li class="page-item" :class="{ disabled: currentPage === 1 }">
            <button class="page-link" @click="changePage(currentPage - 1)">
              &larr; Previous
            </button>
          </li>

          <li
            v-for="page in visiblePages"
            :key="page"
            class="page-item"
            :class="{ active: page === currentPage, disabled: page === '...' }"
          >
            <button
              v-if="page !== '...'"
              class="page-link"
              @click="changePage(page)"
            >
              {{ page }}
            </button>
            <span v-else class="page-link">...</span>
          </li>

          <li class="page-item" :class="{ disabled: currentPage === totalPages }">
            <button class="page-link" @click="changePage(currentPage + 1)">
              Next &rarr;
            </button>
          </li>
        </ul>
      </nav>

      <button class="btn btn-primary" @click="openAddItemModal">
        Add Item
      </button>
    </div>

    <!-- Modals -->
    <AddItemModal @item-added="fetchItems" />
    <ItemDetails :selectedItem="selectedItem" @edit-requested="openEditModal" />
    <EditItem :selectedItem="selectedItem" @item-updated="fetchItems" />
  </div>
</template>

<script>
import AddItemModal from "@/components/AddItem.vue";
import EditItem from "@/components/EditItem.vue";
import ItemDetails from "@/components/ItemDetails.vue";
import { Modal } from "bootstrap";

export default {
  name: "HomePage",
  components: {
    AddItemModal,
    EditItem,
    ItemDetails,
  },
  data() {
    return {
      items: [],
      updatedItemId: null,
      currentPage: 1,
      itemsPerPage: 7,
      searchQuery: "",
      selectedFilter: "all",
      selectedItem: {},
    };
  },
  computed: {
    filteredItems() {
      let filtered = this.items.filter(
        (item) =>
          this.selectedFilter === "all" ||
          item.classification === this.selectedFilter
      );

      const query = this.searchQuery.toLowerCase();
      filtered = filtered.filter((item) => {
        return (
          item.product_name.toLowerCase().includes(query) ||
          item.inventory_number.toLowerCase().includes(query) ||
          item.recipient.toLowerCase().includes(query) ||
          item.classification.toLowerCase().includes(query)
        );
      });

      filtered.sort((a, b) => b.id - a.id);
      return filtered;
    },
    totalPages() {
      return Math.ceil(this.filteredItems.length / this.itemsPerPage);
    },
    paginatedItems() {
      const start = (this.currentPage - 1) * this.itemsPerPage;
      return this.filteredItems.slice(start, start + this.itemsPerPage);
    },
    visiblePages() {
      const total = this.totalPages;
      const maxVisible = 7;
      const tailVisible = 3;
      let pages = [];

      if (total <= maxVisible + tailVisible + 1) {
        for (let i = 1; i <= total; i++) pages.push(i);
      } else {
        for (let i = 1; i <= maxVisible; i++) pages.push(i);
        pages.push("...");
        for (let i = total - tailVisible + 1; i <= total; i++) {
          pages.push(i);
        }
      }

      return pages;
    },
    seCount() {
      return this.items.filter((item) => item.classification === "SE").length;
    },
    ppeCount() {
      return this.items.filter((item) => item.classification === "PPE").length;
    },
  },
  methods: {
    async fetchItems(updatedItemId = null) {
      try {
        const response = await fetch("http://127.0.0.1:8000/api/items/");
        if (!response.ok) {
          throw new Error("Failed to fetch items");
        }
        this.items = await response.json();
        this.currentPage = 1;

        if (updatedItemId) {
          this.updatedItemId = updatedItemId;
          setTimeout(() => {
            this.updatedItemId = null;
          }, 3000);
        }
      } catch (error) {
        console.error("fetchItems error:", error);
      }
    },
    filterBy(type) {
      this.selectedFilter = type;
      this.currentPage = 1;
    },
    openModal(item) {
      this.selectedItem = item || {};
      const modalElement = document.getElementById("itemModal");
      const modal = new Modal(modalElement);
      modal.show();
    },
    openEditModal() {
      this.$nextTick(() => {
        const editModalEl = document.getElementById("editItemModal");
        if (!editModalEl) {
          console.error("Error: EditItem modal element not found!");
          return;
        }
        const editModal = new Modal(editModalEl, { backdrop: "static" });
        editModal.show();
      });
    },
    openEditModalFromTable(item) {
      this.selectedItem = item;
      this.openEditModal();
    },
    async deleteItem(id) {
      if (!confirm("Are you sure you want to delete this item?")) return;
      try {
        const response = await fetch(`http://127.0.0.1:8000/api/items/${id}/`, {
          method: "DELETE",
        });
        if (!response.ok) throw new Error("Failed to delete item");
        await this.fetchItems();
      } catch (err) {
        console.error("Delete error:", err);
        alert("Failed to delete the item.");
      }
    },
    openAddItemModal() {
      document.querySelectorAll(".modal-backdrop").forEach((backdrop) =>
        backdrop.remove()
      );
      const addItemModalEl = document.getElementById("addItemModal");
      if (addItemModalEl) {
        new Modal(addItemModalEl).show();
      }
    },
    changePage(page) {
      if (page >= 1 && page <= this.totalPages) {
        this.currentPage = page;
      }
    },
    getFullImageUrl(path) {
      return `http://127.0.0.1:8000${path}`;
    },
    formatPrice(value) {
      const num = parseFloat(value) || 0;
      return new Intl.NumberFormat("en-US", {
        minimumFractionDigits: 2,
        maximumFractionDigits: 2,
      }).format(num);
    },
    truncateText(text, maxLength) {
      if (!text) return "";
      return text.length > maxLength ? text.substring(0, maxLength) + "..." : text;
    },
  },
  async mounted() {
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
@keyframes fadeHighlight {
  0% {
    background-color: #ff94df;
  }
  100% {
    background-color: transparent;
  }
}
.animate-highlight {
  animation: fadeHighlight 0.1s ease-in-out;
}

.table-wrapper {
  min-height: 530px;
  display: flex;
  flex-direction: column;
  justify-content: space-between;
}

.pagination-footer {
  min-height: 58px;
}
</style>
