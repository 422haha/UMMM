<template>
  <div class="container-wrapper mt-5">
    <div class="container mt-5">
      <h1>Sign in</h1>
      <form @submit.prevent="logIn" class="mt-7">
        <div class="text-subtitle-1 text-medium-emphasis">아이디</div>
        <v-text-field
          variant="outlined"
          placeholder="Id"
          v-model="username"
          color="primary"
          append-inner-icon="mdi-account-outline"
        ></v-text-field>
        <div class="text-subtitle-1 text-medium-emphasis">비밀번호</div>
        <v-text-field
          type="password"
          variant="outlined"
          :type="show ? 'text' : 'password'"
          placeholder="password"
          v-model="password"
          color="primary"
          append-inner-icon="mdi-lock-outline"
        ></v-text-field>
        <div v-if="!isRight">
          <p><span style="color: red;">아이디(로그인 전용 아이디)</span> 또는 <span style="color: red;">비밀번호</span>를 잘못 입력했습니다.</p>
          <p>입력하신 내용을 다시 확인해주세요.</p>
        </div>
        <div class="button-wrapper" style="display: flex; justify-content: flex-end;">
          <v-col cols="auto">
          <v-btn type="submit" icon="mdi-login" size="large" color="primary"></v-btn>
          </v-col>
        </div>
      </form>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useUserStore } from '@/stores/users'

const userStore = useUserStore()

const show = ref(false)
const username = ref('')
const password = ref('')
const isRight = ref(true)

const logIn = () => {
  const payload = {
    username: username.value,
    password: password.value
  }
  const temp = userStore.logIn(payload)

  setTimeout(() => {
    isRight.value = temp
    if (!isRight.value) {
      username.value = ''
      password.value = ''
    }
  }, 200)
}
</script>

<style scoped>
.container-wrapper {
  display: flex;
  justify-content: center;
  width: 100%;
}

.container {
  width: 600px;
  display: flex;
  flex-direction: column;
  margin: 3rem auto;
  padding: 2rem;
}

.button-wrapper {
  margin-top: 1rem;
}
</style>