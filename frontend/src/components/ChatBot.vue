<template>
  <div id="chat-container">
    <div id="chat-messages">
      <div v-for="message in messages" :key="message.id" :class="[message.sender === '나' ? 'send' : 'receive', 'message']">
        <span>{{ message.sender }}: </span>{{ message.content }}
      </div>
    </div>
    <div id="user-input">
      <input 
        type="text" 
        v-model="userMessage" 
        placeholder="메시지를 입력하세요..." 
        @keydown.enter="sendMessage"
      />
      <button @click="sendMessage">전송</button>
      <button @click="$emit('close')">닫기</button>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useUserStore } from '@/stores/users'
import axios from 'axios'

const userStore = useUserStore()
const userMessage = ref('')
const messages = ref([])
const API_KEY = import.meta.env.VITE_CHATGPT_API_KEY
const apiEndpoint = 'https://api.openai.com/v1/chat/completions'

async function fetchAIResponse(messages) {
  const requestOptions = {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      'Authorization': `Bearer ${API_KEY}`
    },
    body: JSON.stringify({
      model: "gpt-3.5-turbo",
      messages,
      temperature: 0.8,
      max_tokens: 1024,
      top_p: 1,
      frequency_penalty: 0.5,
      presence_penalty: 0.5,
      stop: ["Human"]
    })
  }
  
  try {
    const response = await fetch(apiEndpoint, requestOptions)
    const data = await response.json()
    const aiResponse = data.choices[0].message.content
    return aiResponse
  } catch (error) {
    console.error('OpenAI API 호출 중 오류 발생:', error)
    return 'OpenAI API 호출 중 오류 발생'
  }
}

async function sendMessage() {
  const message = userMessage.value.trim()
  if (message.length === 0) return
  
  addMessage('나', message)
  userMessage.value = ''
  
  let aiResponse = ''
  
  // Check for keywords in user input
  const recommendationKeywords = ['추천', '권장', '제안', '추천해줘', '제안해줘', '보여줘', '알려줘']
  const similarityKeywords = ['유사한', '동일한', '비슷한', '같은']
  const introductionKeywords = ['너는 누구', '너 누구', '넌 뭐', '자기소개해봐']
  
  const containsRecommendationKeyword = recommendationKeywords.some(keyword => message.includes(keyword))
  const containsSimilarityKeyword = similarityKeywords.some(keyword => message.includes(keyword))
  const containsIntroductionKeyword = introductionKeywords.some(keyword => message.includes(keyword))

  if (containsIntroductionKeyword) {
    aiResponse = "저는 UMMM 금융 상품 추천 서비스의 마스코트 'MM'이에요!"
  } else if (containsSimilarityKeyword && containsRecommendationKeyword) {
    aiResponse = await getRecommendations()
  } else if (containsRecommendationKeyword) {
    if (message.includes('예금') && message.includes('적금')) {
      aiResponse = await getHighestRateProduct()
    } else if (message.includes('예금')) {
      aiResponse = await getHighestRateDeposit()
    } else if (message.includes('적금')) {
      aiResponse = await getHighestRateSaving()
    } else {
      aiResponse = await getHighestRateProduct()
    }
  } else {
    aiResponse = await fetchAIResponse([{ role: 'user', content: message }])
  }
  
  addMessage('MM', aiResponse)
}

async function getHighestRateProduct() {
  try {
    const response = await axios.get(`${userStore.API_URL}/finlife/highest_rate_product/`)
    const product = response.data
    return `추천 상품은 ${product.fin_prdt_nm} (${product.kor_co_nm}) 입니다!`
  } catch (error) {
    console.error('최고 이자율 상품을 불러오는 중 오류 발생:', error)
    return '최고 이자율 상품을 불러오는 중 오류가 발생했습니다.'
  }
}

async function getHighestRateDeposit() {
  try {
    const response = await axios.get(`${userStore.API_URL}/finlife/highest_deposit/`)
    const deposit = response.data
    return `추천 예금 상품은 ${deposit.fin_prdt_nm} (${deposit.kor_co_nm}) 입니다!`
  } catch (error) {
    console.error('최고 예금 상품을 불러오는 중 오류 발생:', error)
    return '최고 예금 상품을 불러오는 중 오류가 발생했습니다.'
  }
}

async function getHighestRateSaving() {
  try {
    const response = await axios.get(`${userStore.API_URL}/finlife/highest_saving/`)
    const saving = response.data
    return `추천 적금 상품은 ${saving.fin_prdt_nm} (${saving.kor_co_nm}) 입니다!`
  } catch (error) {
    console.error('최고 적금 상품을 불러오는 중 오류 발생:', error)
    return '최고 적금 상품을 불러오는 중 오류가 발생했습니다.'
  }
}

async function getRecommendations() {
  if (!userStore.isLogin) {
    return '로그인 후 이용 가능합니다!'
  }
  try {
    const recommendationResponse = await axios.get(`${userStore.API_URL}/finlife/recommend/`, {
      headers: {
        Authorization: `Token ${userStore.token}`
      }
    })
    const deposits = recommendationResponse.data.recommended_deposits
    const savings = recommendationResponse.data.recommended_savings
    return generateRecommendationResponse(deposits, savings)
  } catch (error) {
    console.error('추천 데이터를 불러오는 중 오류 발생:', error)
    return '추천 데이터를 불러오는 중 오류가 발생했습니다.'
  }
}

function generateRecommendationResponse(deposits, savings) {
  let response = '다음은 추천 상품 목록입니다:\n'
  deposits.forEach(deposit => {
    response += `- ${deposit.fin_prdt_nm} (${deposit.kor_co_nm})\n`
  })
  savings.forEach(saving => {
    response += `- ${saving.fin_prdt_nm} (${saving.kor_co_nm})\n`
  })
  return response
}

function addMessage(sender, content) {
  messages.value.unshift({
    id: Date.now(),
    sender,
    content
  })
}
</script>

<style scoped>
.message {
  border-top: 1px solid #ccc;
  padding: 10px;
  margin-top: 5px;
}

.send {
  background-color: #1e88e5;
  color: white;
}

.receive {
  background-color: #e6e6e6;
}

#chat-container {
  width: 100%;
  height: 100%;
  display: flex;
  flex-direction: column;
  border: 1px solid #ccc;
}

#chat-messages {
  flex: 1;
  overflow-y: auto;
  padding: 10px;
  height: 500px; /* 높이 고정 */
  max-height: 500px; /* 최대 높이 설정 */
  display: flex;
  flex-direction: column-reverse; /* 최신 메시지가 아래에 오도록 설정 */
}

#user-input {
  display: flex;
  padding: 10px;
}

#user-input input {
  flex: 1;
  padding: 10px;
  outline: none;
  background-color: white;
}

#user-input button {
  border: none;
  background-color: #1e88e5;
  color: white;
  padding: 10px 15px;
  cursor: pointer;
}

/* 스크롤바 스타일 설정 */
#chat-messages::-webkit-scrollbar {
  width: 10px;
}

/* 스크롤바 스크롤 버튼 설정 */
#chat-messages::-webkit-scrollbar-thumb {
  background-color: rgba(0, 0, 0, 0.3);
  border-radius: 10px;
}

/* 스크롤바 track(트랙) 설정 */
#chat-messages::-webkit-scrollbar-track {
  background-color: rgba(0, 0, 0, 0.1);
  border-radius: 10px;
}
</style>
