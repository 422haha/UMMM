<template>
  <div>
    <header>
      <Nav></Nav>
      <div class="hr"></div>
    </header>
    <RouterView />
    <Footer class="footer"/>
  </div>
</template>

<script setup>
import Nav from '@/components/Nav.vue'
import Footer from '@/components/Footer.vue'
</script>

<style scoped>
.hr {
  height: 1px;
  background-color: #DBDBDB;
}

.footer {
  position: relative;
  bottom: 40px;
  transform : translateY(100%);
}
</style>

<style>
.color {
  color: #1089FF;
}
</style>