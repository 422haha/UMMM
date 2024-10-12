<template>
  <div class="container-wrapper mt-10">
    <div class="container mt-10">
      <div class="text-subtitle-1 text-medium-emphasis">제목</div>
      <v-text-field
        variant="outlined"
        color="#1089FF"
        placeholder="Title"
        v-model="state.title"
        :error-messages="v$.title.$errors.map(e => e.$message)"
        @input="v$.title.$touch"
        @blur="v$.title.$touch"
        @keypress.enter.prevent="updateArticle"
      ></v-text-field>
      <div class="text-subtitle-1 text-medium-emphasis">내용</div>
      <v-textarea
        variant="outlined"
        color="#1089FF"
        placeholder="Content"
        v-model="state.content"
        auto-grow
        rows="15"
        row-height="25"
        shaped
        :error-messages="v$.content.$errors.map(e => e.$message)"
        @input="v$.content.$touch"
        @blur="v$.content.$touch"
      ></v-textarea>
      <v-btn 
        color="primary"
        class="mt-5 write-btn"
        outlined
        @click.prevent="updateArticle">
        <i class="fa-solid fa-upload icon"></i>
        게시물 수정하기
      </v-btn>
    </div> 
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import { useUserStore } from '@/stores/users'
import { useVuelidate } from '@vuelidate/core'
import { required, maxLength, helpers } from '@vuelidate/validators'
import axios from 'axios'

const initialState = {
  title: '',
  content: ''
}

const state = ref({
  ...initialState
})

const route = useRoute()
const router = useRouter()
const userStore = useUserStore()

const articleId = route.params.id
const pageNum = route.query.page

const rules = {
  title: {
    required: helpers.withMessage('필수 정보입니다.', required),
    maxLength: helpers.withMessage('300자 이하로 입력해야합니다.', maxLength(300))
  },
  content: {
    required: helpers.withMessage('필수 정보입니다.', required),
    maxLength: helpers.withMessage('10000자 이하로 입력해야합니다.', maxLength(10000))
  }
}

const v$ = useVuelidate(rules, state)

onMounted(() => {
  axios({
    method: 'get',
    url: `${userStore.API_URL}/articles/${articleId}/`,
    headers: {
      Authorization: `Token ${userStore.token}`
    }
  })
    .then((res) => {
      state.value.title = res.data.title
      state.value.content = res.data.content
    })
    .catch((err) => {
      console.log(err)
    })
})

const updateArticle = function () {
  v$.value.$validate()

  if (!v$.value.$error) {
    axios({
      method: 'put',
      url: `${userStore.API_URL}/articles/${articleId}/`,
      headers: {
        Authorization: `Token ${userStore.token}`
      },
      data: {
        title: state.value.title,
        content: state.value.content
      }
    })
      .then((res) => {
        router.push({ name: 'articleDetail', params: { id: res.data.id }, query: { page: pageNum } })
      })
      .catch((err) => {
        console.log(err)
      })
  }
}
</script>

<style scoped>
.container-wrapper {
  display: flex;
  justify-content: center;
  width: 100%;
}

.container {
  width: 50%;
  display: flex;
  flex-direction: column;
}

.icon {
  margin-right: 8px;
}
</style>