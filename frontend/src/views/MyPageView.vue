<template>
  <header>
    <div class="text-center">
      <v-avatar size="300" class="mb-5">
        <v-img cover :src="`${userStore.API_URL}${userStore.userInfo.profile_img}`"></v-img>
      </v-avatar>
      <div>
      <h2>반가워요, {{ userStore.userInfo.nickname }}님!</h2>
      </div>

      <div class="buttons-section">
        <v-btn
          prepend-icon="mdi-check-circle"
          :to="{ name: 'profile', params: { username: userStore.userInfo.username }}"
          class="nav-button"
        >
          <template v-slot:prepend>
            <v-icon color="primary"></v-icon>
          </template>
          회원 정보 보기
        </v-btn>
        <v-btn
          prepend-icon="mdi-check-circle"
          :to="{ name: 'productManage', params: { username: userStore.userInfo.username }}"
          class="nav-button"
        >
          <template v-slot:prepend>
            <v-icon color="primary"></v-icon>
          </template>
          가입 상품 관리
        </v-btn>
        <v-btn
          prepend-icon="mdi-check-circle"
          :to="{ name: 'productRecommend', params: { username: userStore.userInfo.username }}"
          class="nav-button"
        >
          <template v-slot:prepend>
            <v-icon color="primary"></v-icon>
          </template>
          상품 추천 받기
        </v-btn>
      </div>
    </div>  
  </header>
  <RouterView />
</template>

<script setup>
import { useUserStore } from '@/stores/users'

const userStore = useUserStore()
</script>

<style scoped>
header {
  display: flex;
  justify-content: center;
  align-items: center;
  margin-top: 40px;
  margin-bottom: 30px;
}
.buttons-section {
  margin-top: 20px; /* 버튼과 h2 사이의 여백 추가 */
}
header .nav-button {
  margin-right: 20px; /* 버튼 사이의 간격 추가 */
}

header .nav-button:last-child {
  margin-right: 0; /* 마지막 버튼 뒤에 여백 제거 */
}
.v-btn--active {
  background-color: #1976d2 !important; /* active 상태일 때 색상 */
  color: white !important; /* active 상태일 때 글자 색상 */
}
</style>