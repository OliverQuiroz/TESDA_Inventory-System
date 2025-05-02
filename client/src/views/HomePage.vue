<template>
  <div class="container-fluid mt-4 px-5">
    <!-- ─── SUMMARY CARDS ─── -->
    <div class="row mb-4">
      <div class="col-md-4">
        <div class="card text-center p-3 filter-card" :class="{ 'active-filter': selectedFilter === 'all' }" @click="filterBy('all')">
          <h4>{{ totalCount }}</h4>
          <p>Total Registered Items</p>
        </div>
      </div>
      <div class="col-md-4">
        <div class="card text-center p-3 filter-card" :class="{ 'active-filter': selectedFilter === 'SE' }" @click="filterBy('SE')">
          <h4>{{ seCount }}</h4>
          <p>(SE) Semi-Expendable</p>
        </div>
      </div>
      <div class="col-md-4">
        <div class="card text-center p-3 filter-card" :class="{ 'active-filter': selectedFilter === 'PPE' }" @click="filterBy('PPE')">
          <h4>{{ ppeCount }}</h4>
          <p>(PPE) Property-Plant & Equipment</p>
        </div>
      </div>
    </div>

    <!-- ─── FILTER BAR ─── -->
    <div class="d-flex align-items-center gap-2 overflow-auto mb-4" style="white-space: nowrap;">
      <div class="btn-group" role="group">
        <button class="btn btn-outline-secondary btn-sm" :disabled="currentPage === 1" @click="changePage(currentPage - 1)">← Prev</button>
            <!-- ✅ Insert this line -->
            <span class="align-self-center px-2 small">
              Page {{ currentPage }} of {{ totalPages }}
            </span>

        <button class="btn btn-outline-secondary btn-sm" :disabled="currentPage === totalPages" @click="changePage(currentPage + 1)">Next →</button>
      </div>

      <input v-model="searchQuery" class="form-control" placeholder="Search" style="width: 1000px; min-width: 250px;" />

      <select v-model="selectedMonth" class="form-select" style="width: 290px;">
        <option value="">All Months</option>
        <option v-for="m in monthOptions" :key="m.value" :value="m.value">{{ m.label }}</option>
      </select>

      <div class="d-flex gap-2">
        <button class="btn btn-outline-secondary btn-sm" @click="downloadPDF" :disabled="!filteredItems.length">
          <i class="bi bi-download"></i> Download PDF
        </button>
        <button class="btn btn-primary btn-sm" @click="openAddItemModal" style="min-width: 160px;">
          <i class="bi bi-plus-circle"></i> Add Item
        </button>
      </div>
    </div>

    <!-- ─── TABLE ─── -->
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
            <th>Actions</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="item in paginatedItems" :key="item.id" class="clickable-row" @click="openModal(item)" :class="{ 'table-success animate-highlight': item.id === updatedItemId }">
          <td>{{ formatDate(item.date_of_acquisition) }}</td>
          <td class="truncate-cell" :title="item.accountable_person">{{ truncateText(item.accountable_person, 15) }}</td>
          <td class="truncate-cell" :title="item.fund">{{ truncateText(item.fund, 15) }}</td>
          <td class="truncate-cell" :title="item.article">{{ truncateText(item.article, 15) }}</td>
          <td class="truncate-cell" :title="item.description">{{ truncateText(item.description, 15) }}</td>
          <td class="truncate-cell" :title="item.uacs_code">{{ truncateText(item.uacs_code, 15) }}</td>
          <td class="truncate-cell" :title="item.uacs_category">{{ truncateText(item.uacs_category, 15) }}</td>
          <td class="text-end" v-html="formatPriceHTML(item.unit_cost)"></td>
          <td class="text-end">{{ item.quantity }}</td>
          <td class="text-end" v-html="formatPriceHTML(item.total_cost)"></td>
          <td class="truncate-cell" :title="item.unit">{{ truncateText(item.unit, 15) }}</td>
          <td class="truncate-cell" :title="item.location">{{ truncateText(item.location, 15) }}</td>
          <td class="truncate-cell" :title="item.property_number">{{ truncateText(item.property_number, 15) }}</td>
          <td class="truncate-cell" :title="item.ics_number">{{ truncateText(item.ics_number, 15) }}</td>
          <td>{{ formatDate(item.date_of_po) }}</td>
          <td class="truncate-cell" :title="item.po_number">{{ truncateText(item.po_number, 15) }}</td>
          <td class="truncate-cell" :title="item.supplier_name">{{ truncateText(item.supplier_name, 15) }}</td>
          <td class="p-1">
            <button class="btn btn-icon btn-icon-edit btn-outline-info" @click.stop="openEditModalFromTable(item)" title="Edit">
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

  <!-- 🔐 PASSWORD MODAL -->
<div class="modal fade" id="passwordModal" tabindex="-1">
  <div class="modal-dialog">
    <div class="modal-content p-3">
      <div class="modal-header border-0">
        <h5 class="modal-title">Enter Password for PDF</h5>
        <button type="button" class="btn-close" data-bs-dismiss="modal"></button>
      </div>
      <div class="modal-body">
        <input type="password" v-model="pdfPassword" class="form-control" placeholder="Enter password" />
      </div>
      <div class="modal-footer">
        <button class="btn btn-secondary" data-bs-dismiss="modal">Cancel</button>
        <button class="btn btn-primary" @click="confirmPasswordAndUpload">Download</button>
      </div>
    </div>
  </div>
</div>

</template>

<script>
import jsPDF from "jspdf";
import autoTable from "jspdf-autotable";
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
      pdfPassword: "",
      selectedItem: {},
      monthOptions: Array.from({ length: 12 }, (_, i) => ({
        value: String(i + 1).padStart(2, "0"),
        label: new Date(0, i).toLocaleString("default", { month: "long" }),
      })),
    };
  },
  computed: {
    filteredItems() {
      let list = this.selectedFilter === "all" ? this.items : this.items.filter((i) => i.uacs_category === this.selectedFilter);
      if (this.selectedMonth) {
        list = list.filter((i) => {
          const month = String(new Date(i.date_of_acquisition).getMonth() + 1).padStart(2, "0");
          return month === this.selectedMonth;
        });
      }
      const q = this.searchQuery.toLowerCase();
      return list.filter((i) =>
        [i.article, i.property_number, i.accountable_person, i.location, i.uacs_category]
          .join(" ")
          .toLowerCase()
          .includes(q)
      ).sort((a, b) => b.id - a.id);
    },
    filteredByDateOnly() {
      let list = [...this.items];
      if (this.selectedMonth) {
        list = list.filter((i) => {
          const month = String(new Date(i.date_of_acquisition).getMonth() + 1).padStart(2, "0");
          return month === this.selectedMonth;
        });
      }
      return list;
    },
    totalCount() {
      return this.filteredByDateOnly.length;
    },
    seCount() {
      return this.filteredByDateOnly.filter((i) => i.uacs_category === "SE").length;
    },
    ppeCount() {
      return this.filteredByDateOnly.filter((i) => i.uacs_category === "PPE").length;
    },
    totalPages() {
      return Math.ceil(this.filteredItems.length / this.itemsPerPage);
    },
    paginatedItems() {
      const start = (this.currentPage - 1) * this.itemsPerPage;
      return this.filteredItems.slice(start, start + this.itemsPerPage);
    },
  },
  methods: {
    truncateText(txt, len) {
      return !txt ? "" : txt.length > len ? txt.slice(0, len) + "…" : txt;
    },
    async fetchItems(highlightId = null) {
      const res = await fetch("http://127.0.0.1:8000/api/items/");
      if (!res.ok) throw new Error();
      this.items = await res.json();
      this.currentPage = 1;
      if (highlightId) {
        this.updatedItemId = highlightId;
        setTimeout(() => (this.updatedItemId = null), 3000);
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
      this.$nextTick(() => new Modal(document.getElementById("editItemModal"), { backdrop: "static" }).show());
    },
    openAddItemModal() {
      document.querySelectorAll(".modal-backdrop").forEach((b) => b.remove());
      new Modal(document.getElementById("addItemModal")).show();
    },
    changePage(p) {
      if (p >= 1 && p <= this.totalPages) this.currentPage = p;
    },
    formatPriceHTML(value) {
      const n = new Intl.NumberFormat("en-PH", { minimumFractionDigits: 2 }).format(parseFloat(value) || 0);
      return `₱&nbsp;${n.replace(/,/g, ",<wbr>")}`;
    },
    formatDate(raw) {
      if (!raw) return "";
      return new Date(raw).toLocaleDateString("en-GB", { day: "2-digit", month: "short", year: "numeric" });
    },
    formatPlainPrice(value) {
      const numeric = String(value).replace(/[^\d.-]/g, "");
      return parseFloat(numeric || 0).toFixed(2);
    },
    downloadPDF() {
      const doc = new jsPDF({ orientation: "landscape" });
      const categoryMap = {
        all: "All Categories",
        SE: "Semi-Expendable",
        PPE: "Property-Plant & Equipment",
      };
      const categoryLabel = categoryMap[this.selectedFilter] || "Unknown Category";
      const sampleDate = this.filteredItems[0]?.date_of_acquisition;
      const year = sampleDate ? new Date(sampleDate).getFullYear() : "";

      let titleText = this.selectedMonth
        ? `${categoryLabel.toUpperCase()} FOR THE MONTH OF ${new Date(0, parseInt(this.selectedMonth) - 1).toLocaleString("default", { month: "long" }).toUpperCase()} ${year}`
        : `${categoryLabel.toUpperCase()} FOR THE YEAR ${year}`;

      const generatedDate = new Date().toLocaleDateString("en-GB", {
        day: "2-digit",
        month: "long",
        year: "numeric",
      });

      doc.setFontSize(14);
      const pageWidth = doc.internal.pageSize.getWidth();
      doc.text(titleText, (pageWidth - doc.getTextWidth(titleText)) / 2, 15);

      doc.setFontSize(10);
      const subtitle = `Generated on ${generatedDate}`;
      doc.text(subtitle, (pageWidth - doc.getTextWidth(subtitle)) / 2, 22);

      const headers = [
        "Date Acq", "Person", "Fund", "Article", "Description", "UACS Code",
        "Category", "Unit Cost", "Qty", "Total Cost", "Unit", "Location",
        "Property No.", "ICS No.", "PO Date", "PO #", "Supplier"
      ];
      const rows = this.filteredItems.map(item => [
        this.formatDate(item.date_of_acquisition),
        item.accountable_person,
        item.fund,
        item.article,
        item.description,
        item.uacs_code,
        item.uacs_category,
        this.formatPlainPrice(item.unit_cost),
        item.quantity,
        this.formatPlainPrice(item.total_cost),
        item.unit,
        item.location,
        item.property_number,
        item.ics_number,
        this.formatDate(item.date_of_po),
        item.po_number,
        item.supplier_name
      ]);

      autoTable(doc, {
        head: [headers],
        body: rows,
        startY: 28,
        margin: { top: 30, bottom: 20, left: 6 },
        styles: { fontSize: 7, cellPadding: 1, overflow: 'linebreak' },
        headStyles: { fillColor: [52, 58, 64], textColor: 255, halign: 'center' },
        columnStyles: {
          0: { cellWidth: 10 }, 1: { cellWidth: 20 }, 2: { cellWidth: 20 },
          3: { cellWidth: 20 }, 4: { cellWidth: 20 }, 5: { cellWidth: 20 },
          6: { cellWidth: 13 }, 7: { cellWidth: 20 }, 8: { cellWidth: 10 },
          9: { cellWidth: 20 }, 10: { cellWidth: 10 }, 11: { cellWidth: 13 },
          12: { cellWidth: 20 }, 13: { cellWidth: 20 }, 14: { cellWidth: 10 },
          15: { cellWidth: 20 }, 16: { cellWidth: 20 }
        },
        theme: 'grid'
      });

      const password = prompt("Enter password to protect the PDF:");
      if (!password) return;

      const pdfBlob = doc.output("blob");
      const formData = new FormData();
      formData.append("pdf", pdfBlob, "Registered_Items.pdf");
      formData.append("password", password);

      fetch("http://localhost:8000/api/protect-pdf/", {
        method: "POST",
        body: formData,
      })
        .then((res) => res.blob())
        .then((protectedBlob) => {
          const url = URL.createObjectURL(protectedBlob);
          const link = document.createElement("a");
          link.href = url;
          link.download = "Protected_Registered_Items.pdf";
          link.click();
        })
        .catch(() => alert("Failed to generate protected PDF."));
    },
  },
  mounted() {
    this.fetchItems();
  },
};
</script>


<style scoped>
.table-squish th,
.table-squish td { font-size: 0.85rem; }
.w-desc { max-width: 240px; word-break: break-word; }
.w-110 { max-width: 110px; }
.w-100 { max-width: 100px; }
.btn-icon { padding: 0.23rem 0.35rem; line-height: 1; }
.btn-icon-edit { font-size: 1rem; padding: 0.4rem 0.35rem; }
.clickable-row { cursor: pointer; }
.active-filter {
  border: 2px solid #007bff;
  background-color: #007bff;
  color: white;
  box-shadow: 0 0 0 0.15rem rgba(0, 123, 255, 0.5);
}
.filter-card:hover { transform: scale(1.05); transition: 0.3s; }
.animate-highlight { animation: fadeHighlight 0.2s ease-in-out; }
@keyframes fadeHighlight { 0% { background: #ff94df; } 100% { background: transparent; } }
.table-wrapper { min-height: 530px; display: flex; flex-direction: column; }

.truncate-cell {
  max-width: 100px;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
  vertical-align: middle;
}

</style>
