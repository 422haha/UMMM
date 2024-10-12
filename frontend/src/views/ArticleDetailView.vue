<template>
  <div class="container-wrapper mt-10">
    <div v-if="article" class="container">
      <v-col cols="auto">
        <v-btn icon="mdi-keyboard-backspace" size="small" elevated @click="goBack"></v-btn>
      </v-col>
      <header>
        <div class="mt-5">
          <h1>{{ article.title }}</h1>
          <div class="profile-container mt-3">      
            <v-avatar class="profile-img" size="large">
              <v-img
                cover
                id="profile-img"
                :src="`${userStore.API_URL}${article.user.profile_img}`"
                alt="profile-img"
              ></v-img>
            </v-avatar>
            <div>
              <p class="mt-6">작성자 : {{ article.user.nickname }}</p>
              <div class="mt-1 mb-1">
                <span>작성일 : 
                  {{ article.created_at.slice(0, 4) }}년 
                  {{ article.created_at.slice(5, 7) }}월 
                  {{ article.created_at.slice(8, 10) }}일 
                  {{ article.created_at.slice(11, 16) }} | 
                </span>
                <span>수정일 : 
                  {{ article.updated_at.slice(0, 4) }}년 
                  {{ article.updated_at.slice(5, 7) }}월 
                  {{ article.updated_at.slice(8, 10) }}일 
                  {{ article.updated_at.slice(11, 16) }} 
                </span>
              </div>
            </div>
          </div>
        </div>
      </header>
      <v-divider></v-divider>

      <main>
        <article class="article">
          <div v-html="article.content"></div>
        </article>
      </main>
      <v-divider></v-divider>
      
      <div v-if="isArticleedUser" class="mt-2">
        <v-btn
          prepend-icon="mdi-pen"
          :to="{ name: 'articleUpdate', params: { id: articleId }, query: { page: pageNum }}"
          >
          <template v-slot:prepend>
            <v-icon color="primary"></v-icon>
          </template>
          수정
        </v-btn>
        <span class="space"></span>
        <v-btn
          prepend-icon="mdi-trash-can-outline"
          @click.prevent="deleteArticle"
          >
          <template v-slot:prepend>
            <v-icon color="red"></v-icon>
          </template>
          삭제
        </v-btn>
      </div>

      <h3 class="mt-10 mb-2">댓글</h3>
      <div v-if="userStore.isLogin">
        <v-form @submit.prevent="createComment" class="flex-form">
          <v-text-field label="댓글을 입력하세요." v-model="commentContent"></v-text-field>
          <v-btn @click.prevent="createComment" class="write-btn">쓰기</v-btn>
        </v-form>
      </div>

      <v-dialog v-model="dialog" width="400">
            <v-card>
              <v-card-title>
                <span>댓글 수정</span>
              </v-card-title>

              <v-card-text>
                <v-text-field
                  v-model="updatedCommentContent"
                  label="댓글"
                  @keypress.enter="save"
                ></v-text-field>
              </v-card-text>

              <v-card-actions>
                <v-btn @click="close">
                  취소
                </v-btn>
                <v-btn @click="save">
                  수정
                </v-btn>
              </v-card-actions>
            </v-card>
          </v-dialog>

      <div v-for="comment in comments" :key="comment.id">
        <div class="mt-5">
          <div class="article">
            <div style="display: flex; justify-content: space-between;">
              <span>작성자 : {{ comment.user.nickname }}</span>
              <span>
                <span> 
                  {{ comment.created_at.slice(0, 4) }}년 
                  {{ comment.created_at.slice(5, 7) }}월 
                  {{ comment.created_at.slice(8, 10) }}일 
                  {{ comment.created_at.slice(11, 16) }}
                </span> 
              </span>
            </div>  
            <div class="mt-3">
              <p v-html="comment.content"></p>
              <div v-if="comment.user.username === userStore.userInfo.username">
                <v-btn
                  prepend-icon="mdi-pen"
                  @click="editComment(comment.id, comment.content)"
                  >
                  <template v-slot:prepend>
                    <v-icon color="primary"></v-icon>
                  </template>
                  수정</v-btn>
                <span class="space"></span>
                <v-btn
                  prepend-icon="mdi-trash-can-outline"
                  @click="deleteComment(comment.id)"
                  >
                  <template v-slot:prepend>
                    <v-icon color="red"></v-icon>
                  </template>
                  삭제</v-btn>
              </div>
            </div>
          </div>
        </div>
        <hr>
      </div>
      
    </div>
    <div v-else>
      <v-progress-circular
        indeterminate
        size="80"
        ></v-progress-circular>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { useUserStore } from '@/stores/users'
import axios from 'axios'

const route = useRoute()
const articleId = route.params.id
const router = useRouter()
const pageNum = route.query.page

const article = ref()
const comments = ref()

const dialog = ref(false)
const isArticleedUser = ref(false)
const commentContent = ref('')
const updatedCommentId = ref()
const updatedCommentContent = ref('')

const userStore = useUserStore()

const getComments = function () {
  axios({
    method: 'get',
    url: `${userStore.API_URL}/articles/${articleId}/comments/`,
    headers: {
      Authorization: `Token ${userStore.token}`
    }
  })
    .then((res) => {
      comments.value = res.data
    })
    .catch((err) => {
      console.log(err)
    })
}

onMounted(() => {
  axios({
      method: 'get',
      url: `${userStore.API_URL}/articles/${articleId}/`,
      headers: {
        Authorization: `Token ${userStore.token}`
      }
    })
      .then((res) => {
        article.value = res.data
        article.value.content = res.data.content.replaceAll("\n", "<br />")
        
        if (article.value.user.username === userStore.userInfo.username) {
          isArticleedUser.value = true
        }
      })
      .catch((err) => {
        console.log(err)
      })

  getComments()
})

const deleteArticle = function () {
  const answer = window.confirm('정말 삭제하시겠습니까?')

  if (answer) {
    axios({
      method: 'delete',
      url: `${userStore.API_URL}/articles/${articleId}/`,
      headers: {
        Authorization: `Token ${userStore.token}`
      }
    })
      .then((res) => {
        router.push({ name: 'articleList', query: { page: pageNum }})
      })
      .catch((err) => {
        console.log(err)
      })
  }
}

const createComment = function () {
  axios({
    method: 'post',
    url: `${userStore.API_URL}/articles/${articleId}/comments/`,
    headers: {
      Authorization: `Token ${userStore.token}`
    },
    data: {
      content: commentContent.value
    }
  })
    .then((res) => {
      comments.value.push(res.data)
      commentContent.value = ''
      setTimeout(() => {
        window.scrollTo({ left: 0, top: document.body.scrollHeight+100, behavior: "smooth" });
      }, 200)
      
    })
    .catch((err) => {
      console.log(err)
    })
}

const deleteComment = function (commentId) {
  const answer = window.confirm('정말 삭제하시겠습니까?')

  if (answer) {
    axios({
      method: 'delete',
      url: `${userStore.API_URL}/articles/${articleId}/comments/${commentId}/`,
      headers: {
        Authorization: `Token ${userStore.token}`
      }
    })
      .then((res) => {
        comments.value = comments.value.filter((comment) => comment.id != commentId)
      })
      .catch((err) => {
        console.log(err)
      })
  }
}

const close = function () {
  dialog.value = false
}

const editComment = function (commentId, value) {
  updatedCommentId.value = commentId
  updatedCommentContent.value = value
  
  dialog.value = true
}

const save = function () {
  axios({
    method: 'put',
    url: `${userStore.API_URL}/articles/${articleId}/comments/${updatedCommentId.value}/`,
    headers: {
      Authorization: `Token ${userStore.token}`
    },
    data: {
      content: updatedCommentContent.value
    }
  })
    .then((res) => {
      getComments()
      dialog.value = false
    })
    .catch((err) => {
      console.log(err)
    })
}

const goBack = function () {
  router.push({ name: 'articleList', query: { page: pageNum }})
}
</script>

<style scoped>
.container-wrapper {
  display: flex;
  justify-content: center;
  width: 100%;
}

.container {
  width: 55%;
  display: flex;
  flex-direction: column;
}

.profile-container {
  display: flex;
  align-items: center;
}

.profile-img {
  margin-right: 5px;
  margin-top: 11px;
}

.article p {
  margin-bottom: 10px;
}

.article {
  padding: 15px;
  border-radius: 5px;
  background-color: #f9f9f9;
  max-width: 100%;
  margin: auto;
  margin-top: 20px;
  margin-bottom: 20px;
}

.space {
  margin: 0 3px;
}

.flex-form {
  display: flex;
  align-items: center;
}

.write-btn{
  margin-bottom: 20px; 
}
</style>