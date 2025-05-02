<template>
  <div class="container-fluid mt-4 px-5">
    <!-- ─── SUMMARY CARDS ─── -->
    <div class="row mb-4 summary-row">
      <div class="col-md-4">
        <div
          class="card text-center p-3 filter-card"
          :class="{ 'active-filter': selectedFilter === 'all' }"
          @click="filterBy('all')"
        >
          <h4>{{ totalCount }}</h4>
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
          <p>(PPE) Property-Plant &amp; Equipment</p>
        </div>
      </div>
    </div>

    <!-- ─── RESPONSIVE FILTER BAR ─── -->
    <!--  < 768 px  → stacked blocks (three “layers”) -->
    <!-- ≥ 768 px  → one horizontal bar (original desktop layout) -->
    <div
      class="filter-bar d-flex flex-column flex-md-row flex-wrap gap-2 mb-4 align-items-start align-items-md-center"
    >
      <!-- Search & Month -->
      <div class="d-flex flex-column flex-md-row gap-2 flex-grow-1">
        <input
          v-model="searchQuery"
          class="form-control flex-grow-1"
          placeholder="Search"
        />
        <select v-model="selectedMonth" class="form-select" style="max-width:260px;">
          <option value="">All Months</option>
          <option
            v-for="m in monthOptions"
            :key="m.value"
            :value="m.value"
          >
            {{ m.label }}
          </option>
        </select>
      </div>

      <!-- Download / Add -->
      <div class="d-flex gap-2">
        <button
          class="btn btn-outline-secondary btn-sm"
          @click="downloadPDF"
          :disabled="!filteredItems.length"
        >
          <i class="bi bi-download"></i> Download PDF
        </button>
        <button
          class="btn btn-primary btn-sm"
          @click="openAddItemModal"
          style="min-width:160px;"
        >
          <i class="bi bi-plus-circle"></i> Add Item
        </button>
      </div>

      <!-- Pagination -->
      <div class="d-flex gap-2 align-items-center ms-md-auto">
        <button
          class="btn btn-outline-secondary btn-sm"
          :disabled="currentPage === 1"
          @click="changePage(currentPage - 1)"
        >
          ← Prev
        </button>

        <span class="small fw-semibold">
          Page {{ currentPage }} of {{ totalPages }}
        </span>

        <button
          class="btn btn-outline-secondary btn-sm"
          :disabled="currentPage === totalPages"
          @click="changePage(currentPage + 1)"
        >
          Next →
        </button>
      </div>
    </div>

    <!-- ─── ITEMS TABLE ─── -->
    <div class="table-wrapper">
      <div class="table-responsive">
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
            <tr
              v-for="item in paginatedItems"
              :key="item.id"
              class="clickable-row"
              @click="openModal(item)"
              :class="{ 'table-success animate-highlight': item.id === updatedItemId }"
            >
              <td>{{ formatDate(item.date_of_acquisition) }}</td>
              <td class="truncate-cell" :title="item.accountable_person">
                {{ truncateText(item.accountable_person, 15) }}
              </td>
              <td class="truncate-cell" :title="item.fund">{{ truncateText(item.fund,15) }}</td>
              <td class="truncate-cell" :title="item.article">{{ truncateText(item.article,15) }}</td>
              <td class="truncate-cell" :title="item.description">{{ truncateText(item.description,15) }}</td>
              <td class="truncate-cell" :title="item.uacs_code">{{ truncateText(item.uacs_code,15) }}</td>
              <td class="truncate-cell" :title="item.uacs_category">{{ truncateText(item.uacs_category,15) }}</td>
              <td class="text-end" v-html="formatPriceHTML(item.unit_cost)" />
              <td class="text-end">{{ item.quantity }}</td>
              <td class="text-end" v-html="formatPriceHTML(item.total_cost)" />
              <td class="truncate-cell" :title="item.unit">{{ truncateText(item.unit,15) }}</td>
              <td class="truncate-cell" :title="item.location">{{ truncateText(item.location,15) }}</td>
              <td class="truncate-cell" :title="item.property_number">{{ truncateText(item.property_number,15) }}</td>
              <td class="truncate-cell" :title="item.ics_number">{{ truncateText(item.ics_number,15) }}</td>
              <td>{{ formatDate(item.date_of_po) }}</td>
              <td class="truncate-cell" :title="item.po_number">{{ truncateText(item.po_number,15) }}</td>
              <td class="truncate-cell" :title="item.supplier_name">{{ truncateText(item.supplier_name,15) }}</td>
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
    </div>

    <!-- ─── MODALS ─── -->
    <AddItemModal @item-added="fetchItems" />
    <ItemDetails :selectedItem="selectedItem" @edit-requested="openEditModal" />
    <EditItem     :selectedItem="selectedItem" @item-updated="fetchItems" />
  </div>

  <!-- 🔐 PASSWORD MODAL -->
  <div class="modal fade" id="passwordModal" tabindex="-1">
    <div class="modal-dialog">
      <div class="modal-content p-3">
        <div class="modal-header border-0">
          <h5 class="modal-title">Enter Password for PDF</h5>
          <button type="button" class="btn-close" data-bs-dismiss="modal" />
        </div>
        <div class="modal-body">
          <input
            type="password"
            v-model="pdfPassword"
            class="form-control"
            placeholder="Enter password"
          />
        </div>
        <div class="modal-footer">
          <button class="btn btn-secondary" data-bs-dismiss="modal">Cancel</button>
          <button class="btn btn-primary" @click="confirmPasswordAndUpload">
            Download
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import jsPDF      from "jspdf";
import autoTable  from "jspdf-autotable";
import { Modal }  from "bootstrap";
import AddItemModal from "@/components/AddItem.vue";
import EditItem     from "@/components/EditItem.vue";
import ItemDetails  from "@/components/ItemDetails.vue";

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

  /* ---------- COMPUTED ---------- */
  computed: {
    filteredItems() {
      let list =
        this.selectedFilter === "all"
          ? this.items
          : this.items.filter((i) => i.uacs_category === this.selectedFilter);

      if (this.selectedMonth) {
        list = list.filter((i) => {
          const m = String(new Date(i.date_of_acquisition).getMonth() + 1).padStart(2, "0");
          return m === this.selectedMonth;
        });
      }
      const q = this.searchQuery.toLowerCase();
      return list
        .filter((i) =>
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
        )
        .sort((a, b) => b.id - a.id);
    },

    filteredByDateOnly() {
      let list = [...this.items];
      if (this.selectedMonth) {
        list = list.filter((i) => {
          const m = String(new Date(i.date_of_acquisition).getMonth() + 1).padStart(2, "0");
          return m === this.selectedMonth;
        });
      }
      return list;
    },

    totalCount() { return this.filteredByDateOnly.length; },
    seCount()    { return this.filteredByDateOnly.filter((i) => i.uacs_category === "SE").length; },
    ppeCount()   { return this.filteredByDateOnly.filter((i) => i.uacs_category === "PPE").length; },

    totalPages() {
      return Math.ceil(this.filteredItems.length / this.itemsPerPage);
    },
    paginatedItems() {
      const start = (this.currentPage - 1) * this.itemsPerPage;
      return this.filteredItems.slice(start, start + this.itemsPerPage);
    },
  },

  /* ---------- METHODS ---------- */
  methods: {
    truncateText(t, n) { return !t ? "" : t.length > n ? t.slice(0, n) + "…" : t; },

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

    filterBy(cat) { this.selectedFilter = cat; this.currentPage = 1; },

    openModal(item) {
      this.selectedItem = item;
      new Modal(document.getElementById("itemModal")).show();
    },
    openEditModalFromTable(item) {
      this.selectedItem = item;
      this.$nextTick(() =>
        new Modal(document.getElementById("editItemModal"), { backdrop: "static" }).show()
      );
    },
    openAddItemModal() {
      document.querySelectorAll(".modal-backdrop").forEach((b) => b.remove());
      new Modal(document.getElementById("addItemModal")).show();
    },
    changePage(p) { if (p >= 1 && p <= this.totalPages) this.currentPage = p; },

    formatPriceHTML(v) {
      const n = new Intl.NumberFormat("en-PH", { minimumFractionDigits: 2 }).format(parseFloat(v) || 0);
      return `₱&nbsp;${n.replace(/,/g, ",<wbr>")}`;
    },
    formatDate(raw) {
      if (!raw) return "";
      return new Date(raw).toLocaleDateString("en-GB", { day: "2-digit", month: "short", year: "numeric" });
    },
    formatPlainPrice(v) {
      const numeric = String(v).replace(/[^\d.-]/g, "");
      return parseFloat(numeric || 0).toFixed(2);
    },

    /* ----- PDF DOWNLOAD (same logic) ----- */
    downloadPDF() {
      const doc = new jsPDF({ orientation: "landscape" });

      const categoryLabel = {
        all: "All Categories",
        SE: "Semi-Expendable",
        PPE: "Property-Plant & Equipment",
      }[this.selectedFilter] || "Unknown Category";

      const year = this.filteredItems[0]
        ? new Date(this.filteredItems[0].date_of_acquisition).getFullYear()
        : "";

      const monthLabel = this.selectedMonth
        ? new Date(0, parseInt(this.selectedMonth) - 1).toLocaleString("default", { month: "long" })
        : "";

      const title = this.selectedMonth
        ? `${categoryLabel.toUpperCase()} FOR THE MONTH OF ${monthLabel.toUpperCase()} ${year}`
        : `${categoryLabel.toUpperCase()} FOR THE YEAR ${year}`;

      const generatedDate = new Date().toLocaleDateString("en-GB", {
        day: "2-digit",
        month: "long",
        year: "numeric",
      });

      /* --- title --- */
      doc.setFontSize(14);
      const pageWidth = doc.internal.pageSize.getWidth();
      doc.text(title, (pageWidth - doc.getTextWidth(title)) / 2, 15);
      doc.setFontSize(10);
      doc.text(`Generated on ${generatedDate}`, (pageWidth - doc.getTextWidth(generatedDate)) / 2, 22);

      /* --- table --- */
      const headers = [
        "Date Acq", "Person", "Fund", "Article", "Description", "UACS Code",
        "Category", "Unit Cost", "Qty", "Total Cost", "Unit", "Location",
        "Property No.", "ICS No.", "PO Date", "PO #", "Supplier"
      ];
      const rows = this.filteredItems.map(i => [
        this.formatDate(i.date_of_acquisition),
        i.accountable_person, i.fund, i.article, i.description, i.uacs_code,
        i.uacs_category, this.formatPlainPrice(i.unit_cost), i.quantity,
        this.formatPlainPrice(i.total_cost), i.unit, i.location,
        i.property_number, i.ics_number, this.formatDate(i.date_of_po),
        i.po_number, i.supplier_name
      ]);

      autoTable(doc, {
        head: [headers], body: rows, startY: 28,
        styles: { fontSize: 7, cellPadding: 1, overflow: "linebreak" },
        headStyles: { fillColor: [52,58,64], textColor: 255, halign: "center" },
        margin: { top: 30, bottom: 20, left: 6 },
        columnStyles: {
          0: { cellWidth: 12 }, 1: { cellWidth: 20 }, 2: { cellWidth: 20 },
          3: { cellWidth: 20 }, 4: { cellWidth: 23 }, 5: { cellWidth: 20 },
          6: { cellWidth: 15 }, 7: { cellWidth: 20 }, 8: { cellWidth: 10 },
          9: { cellWidth: 20 }, 10:{ cellWidth: 10 }, 11:{ cellWidth: 18 },
          12:{ cellWidth: 22 }, 13:{ cellWidth: 18 }, 14:{ cellWidth: 15 },
          15:{ cellWidth: 20 }, 16:{ cellWidth: 25 }
        },
        theme: "grid"
      });

      /* --- password protect via backend endpoint --- */
      const pwd = prompt("Enter password to protect the PDF:");
      if (!pwd) return;

      const blob = doc.output("blob");
      const fd   = new FormData();
      fd.append("pdf", blob, "Registered_Items.pdf");
      fd.append("password", pwd);

      fetch("http://localhost:8000/api/protect-pdf/", { method: "POST", body: fd })
        .then(r => r.blob())
        .then(b => {
          const url = URL.createObjectURL(b);
          const a   = document.createElement("a");
          a.href = url; a.download = "Protected_Registered_Items.pdf"; a.click();
        })
        .catch(() => alert("Failed to generate protected PDF."));
    },

    confirmPasswordAndUpload() {/* optional helper – left as-is */},
  },

  mounted() { this.fetchItems(); },
};
</script>

<style scoped>
.table-squish th,
.table-squish td { font-size:0.85rem; }
.w-desc{ max-width:240px; word-break:break-word; }
.btn-icon      { padding:0.23rem 0.35rem; line-height:1; }
.btn-icon-edit { font-size:1rem; padding:0.4rem 0.35rem; }
.truncate-cell { max-width:100px; overflow:hidden; text-overflow:ellipsis; white-space:nowrap; }
.clickable-row { cursor:pointer; }

.active-filter{
  border:2px solid #007bff; background:#007bff; color:#fff;
  box-shadow:0 0 0 .15rem rgba(0,123,255,.5);
}
.filter-card:hover{ transform:scale(1.05); transition:.3s; }

@keyframes fadeHighlight{0%{background:#ff94df;}100%{background:transparent;}}
.animate-highlight{animation:fadeHighlight .2s ease-in-out;}

.table-wrapper{min-height:530px; display:flex; flex-direction:column;}
.summary-row>div{margin-bottom:1rem;}

/* Mobile tweaks */
@media (max-width:576px){
  .btn-icon-edit{font-size:1.2rem;}
  .table-squish th,.table-squish td{font-size:.75rem;}
}
</style>
