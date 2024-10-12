import { ref } from 'vue'
import { defineStore } from 'pinia'
import axios from 'axios'
import { useUserStore } from '@/stores/users'

export const useArticleStore = defineStore('articles', () => {
  const articles = ref([])
  const totalPage = ref(1)
  const nextLink = ref('')
  const prevLink = ref('')
  const userStore = useUserStore()
  
  const getArticles = function (pageNum=1) {
    const url = pageNum === 1 ? `${userStore.API_URL}/articles/` : `${userStore.API_URL}/articles/?page=${pageNum}`
    axios({
      method: 'get',
      url: url,
      headers: {
        Authorization: `Token ${userStore.token}`
      },
    })
      .then((res) => {
        articles.value = res.data.results
        totalPage.value = Math.ceil(res.data.count / 10)
        nextLink.value = res.data.next
        prevLink.value = res.data.previous
      })
      .catch((err) => {
        console.log(err)
      })
  }

  return { articles, totalPage, nextLink, prevLink, getArticles }
}, { persist: true })