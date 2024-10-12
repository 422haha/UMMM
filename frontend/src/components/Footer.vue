<template>
  <footer class="px-5 py-3 d-flex flex-column align-items-center" @click="scrollToTop">
    <div class="container">
      <img src="@/assets/footer.png" alt="footer" class="logo-img" />
      <div class="text-center mt-1">
        <p class="font-weight-bold mb-1">본 사이트의 콘텐츠는 저작권법의 보호를 받는 바 무단 전재, 복사, 배포 등을 금합니다.</p>
        <p class="font-italic mb-0">Copyright ©UMMM All Rights Reserved.</p>
      </div>    
    </div>
  </footer>
</template>

<script setup>
const scrollToTop = (event) => {
  window.scrollTo({ top: 0, behavior: 'smooth' })
}
</script>

<style scoped>
.container {
  width: 100%;
}

.logo-img {
  width: 200px;
  display: block;
  margin: 10px auto;
  /* margin-bottom: -30px; */
}

footer {
  width: 100%;
  background-color: #ddd;
}
</style>