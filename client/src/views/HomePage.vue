<template>
  <div class="container mt-4">
    <div class="row mb-4">
      <div class="col-md-4">
        <div class="card text-center p-3">
          <i class="bi bi-box-se"></i>
          <h4>100</h4>
          <p>Total Registered Items</p>
        </div>
      </div>
      <div class="col-md-4">
        <div class="card text-center p-3">
          <i class="bi bi-clipboard"></i>
          <h4>70</h4>
          <p> (SE) Semi-Expendable</p>
        </div>
      </div>
      <div class="col-md-4">
        <div class="card text-center p-3">
          <i class="bi bi-clipboard"></i>
          <h4>30</h4>
          <p> (PPE) Property-Plant & Equipment</p>
        </div>
      </div>
    </div>
    
    <div class="d-flex justify-content-between mb-3">
      <input type="text" class="form-control w-25" placeholder="Search" />
    </div>
    
    <table class="table table-bordered text-center">
      <thead>
        <tr>
          <th>Inventory Number</th>
          <th>Product Name</th>
          <th>Description</th>
          <th>Price</th>
          <th>Date of Purchase</th>
          <th>Name of Recipient</th>
          <th>Classification</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="row in 10" :key="row">
          <td>INV-{{ row }}</td>
          <td>Product {{ row }}</td>
          <td>Description of product {{ row }}</td>
          <td>${{ (row * 10).toFixed(2) }}</td>
          <td>2024-02-{{ (row % 28) + 1 }}</td>
          <td>Recipient {{ row }}</td>
          <td>{{ row % 2 === 0 ? 'SE' : 'PPE' }}</td>
        </tr>
      </tbody>
    </table>
    
    <div class="d-flex justify-content-between align-items-center mt-3">
      <nav>
        <ul class="pagination">
          <li class="page-item disabled">
            <span class="page-link">&larr; Previous</span>
          </li>
          <li class="page-item active">
            <span class="page-link">1</span>
          </li>
          <li class="page-item"><a class="page-link" href="#">2</a></li>
          <li class="page-item"><a class="page-link" href="#">3</a></li>
          <li class="page-item disabled"><span class="page-link">...</span></li>
          <li class="page-item"><a class="page-link" href="#">67</a></li>
          <li class="page-item"><a class="page-link" href="#">68</a></li>
          <li class="page-item">
            <a class="page-link" href="#">Next &rarr;</a>
          </li>
        </ul>
      </nav>
      <button class="btn btn-primary">Add Item</button>
    </div>
  </div>
</template>

<script>
export default {
  name: "InventoryPage"
};
</script>

<style scoped>
.card i {
  font-size: 2rem;
}
</style>
