<template>
  <div class="container-wrapper mt-10">
    <div class="container mt-5">
      <v-table>
        <thead>
          <tr>
            <th class="left-align">번호</th>
            <th class="left-align">제목</th>
            <th style="text-align: right;">작성자</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="article in articleStore.articles" :key="article.id" @click="clickTr(article.id)">
            <td class="left-align">{{ article.id }}</td>
            <td class="left-align">{{ article.title }}</td>
            <td class="right-align">
              {{ article.user.nickname }}
              <v-avatar size="small">
                <v-img
                  cover
                  id="profile"
                  :src="`${userStore.API_URL}${article.user.profile_img}`"
                  alt="profile-img"
                ></v-img>
              </v-avatar>
            </td>
          </tr>
        </tbody>
      </v-table>
      <v-btn
        v-if="userStore.isLogin" 
        :to="{ name: 'articleCreate' }" 
        color="primary"
        class="mt-5 write-btn"
        outlined>
        <i class="fa-solid fa-plus icon"></i>
        글 쓰기
      </v-btn>
      <v-pagination v-model="page" :length="articleStore.totalPage" :total-visible="6" class="mt-5"></v-pagination>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, watch } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { useArticleStore } from '@/stores/articles'
import { useUserStore } from '@/stores/users'

const articleStore = useArticleStore()
const userStore = useUserStore()
const route = useRoute()
const router = useRouter()

const queryPage = route.query?.page
const page = ref(Number(queryPage))

watch(page, () => {
  articleStore.getArticles(page.value)
  window.scrollTo({ left: 0, top: 0, behavior: "smooth" });
  router.push({ name: 'articleList', query: { page: page.value }})
})

const clickTr = (articleId) => {
  router.push({ name: 'articleDetail', params: { id: articleId }, query: { page: page.value } })
}

onMounted(() => {
  articleStore.getArticles(page.value)
})
</script>

<style scoped>
.container-wrapper {
  display: flex;
  justify-content: center;
  width: 100%;
}

.container {
  width: 75%;
  display: flex;
  flex-direction: column;
}

.left-align {
  text-align: left;
}

.right-align {
  text-align: right;
}

.icon {
  margin-right: 8px;
}

.write-btn {
  width: 100px;
}
</style>