<template>
  <div class="container-fluid mt-4 px-5">
    <!-- ─── SUMMARY CARDS ─── -->
    <div class="row mb-4">
      <div class="col-md-4">
        <div
          class="card text-center p-3 filter-card"
          :class="{ 'active-filter': selectedFilter === 'all' }"
          @click="filterBy('all')"
        >
          <h4>{{ items.length }}</h4>
          <p>Total Registered Items</p>
        </div>
      </div>
      <div class="col-md-4">
        <div
          class="card text-center p-3 filter-card"
          :class="{ 'active-filter': selectedFilter === 'SE' }"
          @click="filterBy('SE')"
        >
          <h4>{{ seCount }}</h4>
          <p>(SE) Semi-Expendable</p>
        </div>
      </div>
      <div class="col-md-4">
        <div
          class="card text-center p-3 filter-card"
          :class="{ 'active-filter': selectedFilter === 'PPE' }"
          @click="filterBy('PPE')"
        >
          <h4>{{ ppeCount }}</h4>
          <p>(PPE) Property-Plant & Equipment</p>
        </div>
      </div>
    </div>

    <!-- ─── SINGLE ROW FILTER BAR ─── -->
    <div class="d-flex align-items-center gap-2 overflow-auto mb-4" style="white-space: nowrap;">
      <!-- Prev/Next Buttons -->
      <div class="btn-group" role="group">
        <button
          class="btn btn-outline-secondary btn-sm"
          :disabled="currentPage === 1"
          @click="changePage(currentPage - 1)"
        >
          ← Prev
        </button>
        <button
          class="btn btn-outline-secondary btn-sm"
          :disabled="currentPage === totalPages"
          @click="changePage(currentPage + 1)"
        >
          Next →
        </button>
      </div>

      <!-- Search Bar -->
      <input
        v-model="searchQuery"
        class="form-control"
        placeholder="Search"
        style="width: 1000px; min-width: 250px;"
      />

      <!-- Month Filter -->
      <select v-model="selectedMonth" class="form-select" style="width: 160px;">
        <option value="">All Months</option>
        <option v-for="m in monthOptions" :key="m.value" :value="m.value">{{ m.label }}</option>
      </select>

      <!-- Add Item Button -->
      <button class="btn btn-primary btn-sm" @click="openAddItemModal" style="min-width: 120px;">
        Add Item
      </button>
    </div>

    <!-- ─── ITEMS TABLE ─── -->
    <div class="table-wrapper">
      <table class="table table-bordered align-middle text-center table-squish">
        <thead class="table-light small">
          <tr>
            <th>Date<br />of Acq.</th>
            <th>Accountable<br />Person</th>
            <th>Fund</th>
            <th>Article</th>
            <th class="w-desc">Description</th>
            <th>UACS Code</th>
            <th>Category<br />(UACS)</th>
            <th class="text-end">Unit Cost</th>
            <th class="text-end">Qty</th>
            <th class="text-end">Total Cost</th>
            <th>Unit</th>
            <th>Location</th>
            <th>Property No.</th>
            <th>ICS No.</th>
            <th>Date of PO</th>
            <th>PO #</th>
            <th>Supplier</th>
            <th style="width:34px;">Actions</th>
          </tr>
        </thead>

        <tbody>
          <tr
            v-for="item in paginatedItems"
            :key="item.id"
            class="clickable-row"
            @click="openModal(item)"
            :class="{ 'table-success animate-highlight': item.id === updatedItemId }"
          >
            <td>{{ formatDate(item.date_of_acquisition) }}</td>
            <td>{{ item.accountable_person }}</td>
            <td>{{ item.fund }}</td>
            <td>{{ item.article }}</td>
            <td class="text-wrap w-desc">{{ truncateText(item.description, 60) }}</td>
            <td>
              <span class="d-inline-block text-truncate w-110" :title="item.uacs_code">
                {{ item.uacs_code }}
              </span>
            </td>
            <td>{{ item.uacs_category }}</td>
            <td class="text-end" v-html="formatPriceHTML(item.unit_cost)"></td>
            <td class="text-end">{{ item.quantity }}</td>
            <td class="text-end" v-html="formatPriceHTML(item.total_cost)"></td>
            <td>{{ item.unit }}</td>
            <td>{{ item.location }}</td>
            <td>
              <span class="d-inline-block text-truncate w-110" :title="item.property_number">
                {{ item.property_number }}
              </span>
            </td>
            <td>{{ item.ics_number }}</td>
            <td>{{ formatDate(item.date_of_po) }}</td>
            <td>
              <span class="d-inline-block text-truncate w-100" :title="item.po_number">
                {{ item.po_number }}
              </span>
            </td>
            <td>{{ item.supplier_name }}</td>
            <td class="p-1">
              <button
                class="btn btn-icon btn-icon-edit btn-outline-info"
                @click.stop="openEditModalFromTable(item)"
                title="Edit"
              >
                <i class="bi bi-pencil-square"></i>
              </button>
            </td>
          </tr>
          <tr v-if="paginatedItems.length === 0">
            <td colspan="18" class="text-muted text-center">No items found.</td>
          </tr>
        </tbody>
      </table>
    </div>

    <!-- ─── MODALS ─── -->
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
  components: { AddItemModal, EditItem, ItemDetails },
  data() {
    return {
      items: [],
      updatedItemId: null,
      currentPage: 1,
      itemsPerPage: 7,
      searchQuery: "",
      selectedFilter: "all",
      selectedMonth: "",
      selectedItem: {},
      monthOptions: [
        { value: "01", label: "January" },
        { value: "02", label: "February" },
        { value: "03", label: "March" },
        { value: "04", label: "April" },
        { value: "05", label: "May" },
        { value: "06", label: "June" },
        { value: "07", label: "July" },
        { value: "08", label: "August" },
        { value: "09", label: "September" },
        { value: "10", label: "October" },
        { value: "11", label: "November" },
        { value: "12", label: "December" },
      ],
    };
  },
  computed: {
    filteredItems() {
      let list =
        this.selectedFilter === "all"
          ? this.items
          : this.items.filter((i) => i.uacs_category === this.selectedFilter);

      if (this.selectedMonth) {
        list = list.filter((i) => {
          const date = new Date(i.date_of_acquisition);
          const month = String(date.getMonth() + 1).padStart(2, "0");
          return month === this.selectedMonth;
        });
      }

      const q = this.searchQuery.toLowerCase();
      list = list.filter((i) =>
        [
          i.article,
          i.property_number,
          i.accountable_person,
          i.location,
          i.uacs_category,
        ]
          .join(" ")
          .toLowerCase()
          .includes(q)
      );

      return list.sort((a, b) => b.id - a.id);
    },
    totalPages() {
      return Math.ceil(this.filteredItems.length / this.itemsPerPage);
    },
    paginatedItems() {
      const start = (this.currentPage - 1) * this.itemsPerPage;
      return this.filteredItems.slice(start, start + this.itemsPerPage);
    },
    seCount() {
      return this.items.filter((i) => i.uacs_category === "SE").length;
    },
    ppeCount() {
      return this.items.filter((i) => i.uacs_category === "PPE").length;
    },
  },
  methods: {
    async fetchItems(highlightId = null) {
      try {
        const res = await fetch("http://127.0.0.1:8000/api/items/");
        if (!res.ok) throw new Error();
        this.items = await res.json();
        this.currentPage = 1;
        if (highlightId) {
          this.updatedItemId = highlightId;
          setTimeout(() => (this.updatedItemId = null), 3000);
        }
      } catch (e) {
        console.error(e);
      }
    },
    filterBy(cat) {
      this.selectedFilter = cat;
      this.currentPage = 1;
    },
    openModal(item) {
      this.selectedItem = item;
      new Modal(document.getElementById("itemModal")).show();
    },
    openEditModalFromTable(item) {
      this.selectedItem = item;
      this.$nextTick(() =>
        new Modal(document.getElementById("editItemModal"), {
          backdrop: "static",
        }).show()
      );
    },
    openAddItemModal() {
      document.querySelectorAll(".modal-backdrop").forEach((b) => b.remove());
      new Modal(document.getElementById("addItemModal")).show();
    },
    changePage(p) {
      if (p >= 1 && p <= this.totalPages) this.currentPage = p;
    },
    formatPriceHTML(value) {
      const n = new Intl.NumberFormat("en-PH", {
        minimumFractionDigits: 2,
      }).format(parseFloat(value) || 0);
      return `₱&nbsp;${n.replace(/,/g, ",<wbr>")}`;
    },
    formatDate(raw) {
      if (!raw) return "";
      return new Date(raw).toLocaleDateString("en-GB", {
        day: "2-digit",
        month: "short",
        year: "numeric",
      });
    },
    truncateText(txt, len) {
      return !txt ? "" : txt.length > len ? txt.slice(0, len) + "…" : txt;
    },
  },
  mounted() {
    this.fetchItems();
  },
};
</script>


<style scoped>
.table-squish th,
.table-squish td {
  font-size: 0.85rem;
}
.w-desc {
  max-width: 240px;
  word-break: break-word;
}
.w-110 {
  max-width: 110px;
}
.w-100 {
  max-width: 100px;
}
.btn-icon {
  padding: 0.23rem 0.35rem;
  line-height: 1;
}
.btn-icon-edit {
  font-size: 1rem;
  padding: 0.4rem 0.35rem;
}
.clickable-row {
  cursor: pointer;
}
.active-filter {
  border: 2px solid #cce5ff;
  background-color: #e7f1ff;
  box-shadow: 0 0 0 0.1rem #f0f8ff;
  height: 100%;
  min-height: 130px;
  display: flex;
  flex-direction: column;
  justify-content: center;
}
.filter-card {
  height: 100%;
  min-height: 100px;
  display: flex;
  flex-direction: column;
  justify-content: center;
  cursor: pointer;
  transition: 0.3s;
}
.filter-card:hover {
  background: #f8f9fa;
  transform: scale(1.05);
}
@keyframes fadeHighlight {
  0% {
    background: #ff94df;
  }
  100% {
    background: transparent;
  }
}
.animate-highlight {
  animation: fadeHighlight 0.2s ease-in-out;
}
.table-wrapper {
  min-height: 530px;
  display: flex;
  flex-direction: column;
}
</style>
