<template>
  <div class="container">
    <v-carousel
      cycle
      progress="primary"
      hide-delimiters
      show-arrows="hover"
      height="700"
    >
      <v-carousel-item>
        <img src="@/assets/carousel-1.jpg" class="caro-item-img">
      </v-carousel-item>

      <v-carousel-item>
        <img src="@/assets/carousel-2.jpg" class="caro-item-img">
      </v-carousel-item>

      <v-carousel-item>
        <img src="@/assets/carousel-3.jpg" class="caro-item-img">
      </v-carousel-item>
    </v-carousel>
  </div>

  <div>
    <v-btn
      block
      color="#1089FF"
      class="caro-text-btn"
      :to="userStore.isLogin ? { name: 'productRecommend', params: { username: userStore.userInfo.username }} : { name: 'signUp' }"
    >
      회원가입하면 맞춤형 예적금 상품이 팡팡!
    </v-btn>
  </div>
  <div>
    <ChatBotIcon />
  </div>
  <div class="recommendations-container mt-15">
    <div class="recommendations mt-10">
      <div class="card-section">
        <div class="d-flex">
          <h2>금리 높은 <span style="color: dodgerblue;">예금</span> 상품</h2>
          <v-icon class="cart-img" color="#FFC107" icon="mdi-cart-heart"></v-icon>
        </div>
        <div class="card">
          <ol>
            <li v-for="(deposit, index) in topDeposits.slice(0, 5)" :key="deposit.deposit_code">
              <strong>{{ index + 1 }}. {{ deposit.fin_prdt_nm }}</strong> - {{ deposit.kor_co_nm }}
            </li>
          </ol>
        </div>
      </div>

      <div class="card-section">
        <div class="d-flex">
          <h2>금리 높은 <span style="color: dodgerblue;">적금</span> 상품</h2>
          <v-icon class="cart-img" color="#FFC107" icon="mdi-cart-heart"></v-icon>
        </div>
        <div class="card">
          <ol>
            <li v-for="(saving, index) in topSavings.slice(0, 5)" :key="saving.saving_code">
              <strong>{{ index + 1 }}. {{ saving.fin_prdt_nm }}</strong> - {{ saving.kor_co_nm }}
            </li>
          </ol>
        </div>
      </div>

      <div class="card-section">
        <div class="d-flex">
          <h2>UMMM <span style="color: dodgerblue;">추천</span> 상품</h2>
          <v-icon class="cart-img" color="#FFC107" icon="mdi-cart-heart"></v-icon>
        </div>
        <div class="card">
          <ol>
            <li v-for="(product, index) in randomProducts" :key="product.deposit_code || product.saving_code">
              <strong>{{ index + 1 }}. {{ product.fin_prdt_nm }}</strong> - {{ product.kor_co_nm }}
            </li>
          </ol>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useUserStore } from '@/stores/users'
import axios from 'axios'
import ChatBotIcon from '@/components/ChatBotIcon.vue'

const userStore = useUserStore()
const topDeposits = ref([])
const topSavings = ref([])
const randomProducts = ref([])

const fetchRecommendations = async () => {
  try {
    const response = await axios.get(`${userStore.API_URL}/finlife/recommend_chart/`)
    topDeposits.value = response.data.top_deposits
    topSavings.value = response.data.top_savings
    randomProducts.value = response.data.random_products
  } catch (error) {
    console.error('추천 데이터를 불러오는 중 오류 발생:', error)
  }
}

onMounted(fetchRecommendations)
</script>


<style scoped>
.caro-item-img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.caro-text-btn {
  border-radius: 0;
  height: 43px;
}

.recommendations-container {
  display: flex;
  justify-content: center;
  margin-top: 20px;
  width: 100%;
}

.recommendations {
  display: flex;
  justify-content: center;
  gap: 90px;
  width: 90%;
}

.card-section {
  display: flex;
  flex-direction: column;
  align-items: center;
  width: 30%;
}

.card {
  display: flex;
  flex-direction: column;
  height: 100%;
  margin-top: 25px;
  padding: 20px;
  width: 100%;
  border-radius: 5px;
  box-shadow: 0 2px 5px rgba(0,0,0,0.2);
}

.card ol {
  list-style: none;
  padding: 0;
  margin: 0;
}

.card li {
  margin-bottom: 10px;
}

.card h3 {
  margin: 0;
  font-size: 1.2em;
}

.card p {
  margin: 10px 0 0;
  color: #666;
}

.cart-img {
  margin-left: 7px;
  margin-top: 6px;
}
</style>