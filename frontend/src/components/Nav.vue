<template>
  <div class="nav">
    <RouterLink class="logo" :to="{ name: 'home' }">
      <img src="@/assets/logo.png" alt="logo" width="120" />
    </RouterLink>
    <div v-if="!userStore.isLogin" class="sign">
      <v-layout class="overflow-visible" style="height: 80px">
        <v-toolbar flat color="transparent">
          <v-spacer></v-spacer>
          <v-btn text><RouterLink :to="{ name: 'signIn'}" class="link">로그인</RouterLink></v-btn>
          <v-btn text><RouterLink :to="{ name: 'signUp'}" class="link">회원가입</RouterLink></v-btn>
        </v-toolbar>
      </v-layout>
    </div>
    <div v-else class="sign">
      <v-layout class="overflow-visible">
        <v-toolbar flat color="transparent">
          <v-spacer></v-spacer>
            <v-avatar size="small" class="profile-img">
              <v-img
                cover
                id="profile"
                :src="`${userStore.API_URL}${userStore.userInfo.profile_img}`"
                alt="profile-img"
              ></v-img>
            </v-avatar>
            <p text>안녕하세요, {{ userStore.userInfo.nickname }}님</p>
            <v-btn text class="my-page-btn"><RouterLink :to="{ name: 'profile', params: { username: userStore.userInfo.username }}" class="link">마이페이지</RouterLink></v-btn>
            <v-btn text @click.prevent="userStore.logOut"><p class="logout-font">로그아웃</p></v-btn>
        </v-toolbar>
      </v-layout>
    </div>
  </div>

  <div class="bottom-bar">
      <RouterLink :to="{ name: 'depositList' }">금리비교</RouterLink>
      <RouterLink :to="{ name: 'exchange' }">환율계산</RouterLink>
      <RouterLink :to="{ name: 'map' }">주변은행</RouterLink>
      <RouterLink :to="{ name: 'articleList', query: { page: 1 } }">커뮤니티</RouterLink>
    </div>
</template>

<script setup>
import { useUserStore } from '@/stores/users'

const userStore = useUserStore()
</script>

<style scoped>
.nav {
  height: 80px;
  display: flex;
  align-items: center;
}

.logo {
  display: flex;
  align-items: center;
  margin: 0 1rem;
}

.logo img {
  height: 36px;
}

.profile-img {
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.05);
  border-radius: 50%;
}

.bottom-bar {
  background-color: #f0f0f0;
  display: flex;
  justify-content: space-around;
  padding: 10px 0;
}

.bottom-bar a {
  text-decoration: none;
  color: #222;
  font-weight: 600;
}

.menus a {
  font-weight: 600;
  font-size: 20px;
  letter-spacing: -1px;
  color: #222;
  text-decoration: none;
}

.sign {
  margin: 5px 1rem 0 auto;
}

.sign * {
  margin: 5px;
}

.link {
  color: black;
  text-decoration: none;
  font-size: 16px;
  margin: 10px 0;
}

.card {
  width: 180px;
}

.my-page-btn {
  margin-top: -1px;
}

.logout-font {
  font-size: 111%;
}
</style>
