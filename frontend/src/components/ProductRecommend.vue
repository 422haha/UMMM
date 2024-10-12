<template>
  <div class="outer-container">
    <h3 class="mt-5">나와 비슷한 <span style="color: dodgerblue;">나이, 자산, 연봉</span>인 사용자가 많이 가입한 상품은?</h3>
    <div class="full-screen-container">
      <div class="product-card">
        <h3>
          <span><v-icon color="#FFC107" icon="mdi-piggy-bank-outline"></v-icon></span>
          예금
        </h3>
        <ul class="mt-4">
          <template v-if="recommendedDeposits.length > 0">
            <li v-for="deposit in recommendedDeposits" :key="deposit.id">
              <p style="color: dodgerblue;" @click="clickDetail(deposit, '정기예금')">{{ deposit.fin_prdt_nm }} ({{ deposit.kor_co_nm }}) <span><v-icon color="#FFC107" icon="mdi-hand-pointing-left"></v-icon></span></p>
            </li>
          </template>
          <p v-else>해당 사용자가 가입한 상품이 없습니다.</p>
        </ul>
      </div>
      <div class="product-card">
        <h3>
          <span><v-icon color="#FFC107" icon="mdi-piggy-bank-outline"></v-icon></span>
          적금
        </h3>
        <ul class="mt-4">
          <template v-if="recommendedSavings.length > 0">
            <li v-for="saving in recommendedSavings" :key="saving.id">
              <p style="color: dodgerblue;" @click="clickDetail(saving, '정기적금')">{{ saving.fin_prdt_nm }} ({{ saving.kor_co_nm }}) <span><v-icon color="#FFC107" icon="mdi-hand-pointing-left"></v-icon></span></p>
            </li>
          </template>
          <p v-else>해당 사용자가 가입한 상품이 없습니다.</p>
        </ul>
      </div>
    </div>

    <!-- 상품 상세 모달 -->
    <v-dialog v-model="dialog" width="900">
      <v-card v-if="selectedProduct" class="py-5 px-3">
        <v-card-title class="d-flex align-center justify-space-between">
          <div class="d-flex">
            <v-icon color="#FFC107" icon="mdi-piggy-bank-outline"></v-icon>
            <h3 class="ml-3">{{ selectedProduct.fin_prdt_nm }}</h3>
          </div>
          <div v-if="userStore.isLogin">
            <v-btn
              v-if="isContractProduct"
              color="red"
              variant="flat"
              @click.prevent="deleteProductUser(selectedProductType)"
            >가입 취소하기</v-btn>
            <v-btn
              v-else
              color="primary"
              variant="flat"
              @click.prevent="addProductUser(selectedProductType)"
            >가입하기</v-btn>
          </div>
        </v-card-title>
        <div class="mt-5">
          <div class="product-info">
            <p class="mb-2"><strong>금융 회사명 :</strong> {{ selectedProduct.kor_co_nm || '정보 없음' }}</p>
            <p class="mb-2"><strong>가입 방법 :</strong> {{ selectedProduct.join_way || '정보 없음' }}</p>
            <p class="mb-2"><strong>만기 후 이자율 :</strong> {{ selectedProduct.mtrt_int || '정보 없음' }}</p>
            <p class="mb-2"><strong>우대 조건 :</strong> {{ selectedProduct.spcl_cnd || '정보 없음' }}</p>
            <p class="mb-2"><strong>가입 제한 :</strong> {{ selectedProduct.join_deny === 1 ? '가입 가능' : selectedProduct.join_deny === 2 ? '서민 전용' : '일부 제한' }}</p>
            <p class="mb-2"><strong>가입 대상 :</strong> {{ selectedProduct.join_member || '정보 없음' }}</p>
            <p class="mb-2"><strong>기타 사항 :</strong> {{ selectedProduct.etc_note || '정보 없음' }}</p>
            <p class="mb-2"><strong>최고 한도 :</strong> {{ selectedProduct.max_limit ? selectedProduct.max_limit.toString().replace(/\B(?=(\d{3})+(?!\d))/g, ",") : '정보 없음' }}</p>
          </div>
        </div>
        <v-card-actions>
          <v-spacer></v-spacer>
          <v-btn color="#1089FF" variant="text" @click="closeModal">
            닫기
          </v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>
  </div>
</template>

<script setup>
import { ref, onMounted, computed } from 'vue'
import { useUserStore } from '@/stores/users'
import axios from 'axios'
import { useRouter } from 'vue-router'

const userStore = useUserStore()
const router = useRouter()

const loading = ref(true)
const recommendedDeposits = ref([])
const recommendedSavings = ref([])

const dialog = ref(false)
const selectedProduct = ref(null)
const selectedProductCode = ref(null)
const selectedProductType = ref(null)

onMounted(async () => {
  try {
    const response = await axios.get(`${userStore.API_URL}/finlife/recommend/`, {
      headers: {
        Authorization: `Token ${userStore.token}`
      }
    })
    recommendedDeposits.value = response.data.recommended_deposits
    recommendedSavings.value = response.data.recommended_savings
  } catch (error) {
    console.error('Error fetching recommendations:', error)
  } finally {
    loading.value = false
  }
})

const closeModal = () => {
  dialog.value = false
}

const isContractProduct = computed(() => {
  if (!userStore.userInfo || !userStore.userContractDeposits || !userStore.userContractSavings) {
    return false;
  }
  return userStore.userContractDeposits.some(d => d.deposit_code === selectedProductCode.value) || userStore.userContractSavings.some(s => s.saving_code === selectedProductCode.value);
})

const clickDetail = (data, type) => {
  selectedProduct.value = data
  selectedProductCode.value = data.deposit_code || data.saving_code;
  selectedProductType.value = type
  dialog.value = true
}

// Saving 가입하기 함수
const addSavingUser = async () => {
  try {
    await axios({
      method: 'post',
      url: `${userStore.API_URL}/finlife/saving_list/${selectedProductCode.value}/contract/`,
      headers: {
        Authorization: `Token ${userStore.token}`
      }
    })
    alert('저장이 완료되었습니다.')
    await userStore.getUserInfo(userStore.userInfo.username)
    const answer = window.confirm('가입이 완료되었습니다. 가입 상품 관리 페이지로 이동하시겠습니까?')
    if (answer) {
      router.push({ name: 'productManage', params: { username: userStore.userInfo.username }})
    }
  } catch (err) {
    console.log(err)
  }
}

// Deposit 가입하기 함수
const addDepositUser = async () => {
  try {
    await axios({
      method: 'post',
      url: `${userStore.API_URL}/finlife/deposit_list/${selectedProductCode.value}/contract/`,
      headers: {
        Authorization: `Token ${userStore.token}`
      }
    })
    alert('저장이 완료되었습니다.')
    await userStore.getUserInfo(userStore.userInfo.username)
    const answer = window.confirm('가입이 완료되었습니다. 가입 상품 관리 페이지로 이동하시겠습니까?')
    if (answer) {
      router.push({ name: 'productManage', params: { username: userStore.userInfo.username }})
    }
  } catch (err) {
    console.log(err)
  }
}

// Add product user 함수
const addProductUser = async (type) => {
  if (type === '정기예금') {
    await addDepositUser()
  } else {
    await addSavingUser()
  }
}

// 가입 취소하기 함수
const deleteDepositUser = async () => {
  const answer = window.confirm('가입을 취소하시겠습니까?');
  if (answer) {
    try {
      await axios({
        method: 'delete',
        url: `${userStore.API_URL}/finlife/deposit_list/${selectedProductCode.value}/contract/`,
        headers: {
          Authorization: `Token ${userStore.token}`
        }
      })
      await userStore.getUserInfo(userStore.userInfo.username)
    } catch (err) {
      console.log(err)
    }
  }
}

// 가입 취소하기 함수
const deleteSavingUser = async () => {
  const answer = window.confirm('가입을 취소하시겠습니까?');
  if (answer) {
    try {
      await axios({
        method: 'delete',
        url: `${userStore.API_URL}/finlife/saving_list/${selectedProductCode.value}/contract/`,
        headers: {
          Authorization: `Token ${userStore.token}`
        }
      })
      await userStore.getUserInfo(userStore.userInfo.username)
    } catch (err) {
      console.log(err)
    }
  }
}

// Delete product user 함수
const deleteProductUser = async (type) => {
  if (type === '정기예금') {
    await deleteDepositUser()
  } else {
    await deleteSavingUser()
  }
}
</script>

<style scoped>
.outer-container {
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  min-height: 100vh;
  box-sizing: border-box;
}

.full-screen-container {
  display: flex;
  flex-direction: column;
  width: 500px;
  padding-top: 20px;
  min-height: 100vh;
  box-sizing: border-box;
  padding-bottom: 20px;
}

.product-card {
  text-align: left;
  padding: 20px;
  border-radius: 5px;
  width: 100%;
  margin: auto;
  margin-top: 15px;
  margin-bottom: 25px;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
}

ul {
  list-style-type: none;
  padding: 0;
}

li {
  margin-bottom: 10px;
}

button {
  background: none;
  border: none;
  color: #1089FF;
  cursor: pointer;
  text-decoration: underline;
}

button:hover {
  color: #0056b3;
}

.product-info, .product-option-info {
  padding: 20px;
  border: 1px solid #ccc;
  border-radius: 5px;
  background-color: #f9f9f9;
  max-width: 90%;
  margin: auto;
  margin-bottom: 20px;
}

.options-container {
  display: flex;
  flex-wrap: wrap;
  gap: 20px;
  justify-content: flex-start;
}

.option-card {
  flex: 0 0 calc(33.333% - 20px); /* 3개씩 배치하고, 카드 사이 간격을 위해 20px 차감 */
  box-sizing: border-box;
  border: 1px solid #ccc;
  border-radius: 5px;
  padding: 15px;
  background-color: #fff;
  box-shadow: 0 2px 5px rgba(0, 0, 0, 0.1);
}

.option-card p {
  margin-bottom: 10px;
}
</style>