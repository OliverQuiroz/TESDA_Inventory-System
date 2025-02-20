<template>
  <div class="container d-flex flex-column align-items-center justify-content-center mt-5">
    <div class="text-center position-relative">
      <i class="bi bi-qr-code-scan faded-icon"></i>
      <h4 class="mt-3">Scan Now</h4>
      <button class="btn btn-primary mt-3" @click="startScan">Scan Now</button>
    </div>
  </div>
</template>

<script>
export default {
  name: "ScanPage",
  methods: {
    startScan() {
      console.log("Scanning started...");
      // Logic for scanning goes here
    }
  }
};
</script>

<style scoped>
.container {
  height: 70vh;
}
.faded-icon {
  font-size: 8rem;
  opacity: 0.1;
  display: block;
  position: relative;
  top: 0;
  margin-bottom: -40px;
}
</style>
