<template>
  <div class="full-screen-container">
    <!-- 상품 리스트 및 상세 모달 -->
    <v-dialog v-model="dialog" width="900">
      <v-card v-if="selectedProduct" class="py-5 px-3">
        <v-card-title class="d-flex align-center justify-space-between">
          <div class="d-flex">
            <v-icon color="#FFC107" icon="mdi-piggy-bank-outline"></v-icon>
            <h3 class="ml-3">{{ selectedProduct.fin_prdt_nm }}</h3>
          </div>  
          <div v-if="userStore.isLogin">
            <v-btn
              color="red"
              variant="flat"
              @click.prevent="deleteProductUser(selectedProduct)"
            >가입 취소하기</v-btn>
          </div>
        </v-card-title>
        <div class="mt-5">
          <div class="product-info">
            <p><strong>금융 회사명 :</strong> {{ selectedProduct.kor_co_nm || '정보 없음' }}</p>
            <p><strong>가입 방법 :</strong> {{ selectedProduct.join_way || '정보 없음' }}</p>
            <p><strong>만기 후 이자율 :</strong> {{ selectedProduct.mtrt_int || '정보 없음' }}</p>
            <p><strong>우대 조건 :</strong> {{ selectedProduct.spcl_cnd || '정보 없음' }}</p>
            <p><strong>가입 제한 :</strong> {{ selectedProduct.join_deny === 1 ? '가입 가능' : selectedProduct.join_deny === 2 ? '서민 전용' : '일부 제한' }}</p>
            <p><strong>가입 대상 :</strong> {{ selectedProduct.join_member || '정보 없음' }}</p>
            <p><strong>기타 사항 :</strong> {{ selectedProduct.etc_note || '정보 없음' }}</p>
            <p><strong>최고 한도 :</strong> {{ selectedProduct.max_limit ? selectedProduct.max_limit.toString().replace(/\B(?=(\d{3})+(?!\d))/g, ",") : '정보 없음' }}</p>
          </div>
          <div class="product-option-info">
            <p class="mb-4"><strong>금융 상품 옵션</strong></p>
            <div class="options-container">
              <div v-for="(option, index) in selectedProduct.options" :key="index" class="option-card">
                <p v-if="option.rsrv_type_nm"><strong>이자율 유형 :</strong> {{ option.rsrv_type_nm }}</p>
                <p><strong>저축 기간 :</strong> {{ option.save_trm || '정보 없음' }}개월</p>
                <p><strong>저축 금리 :</strong> {{ option.intr_rate || '정보 없음' }}%</p>
                <p><strong>최고 우대 금리 :</strong> {{ option.intr_rate2 || '정보 없음' }}%</p>
              </div>
            </div>
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

    <!-- 상품 리스트 -->
    <div class="content-container">
      <div v-if="products.length !== 0">
        <div class="list-container">
          <p v-for="product in products" :key="product.code" class="product-item">
            {{ product.id }}. ({{ product.type }}) {{ product.kor_co_nm }} - {{ product.fin_prdt_nm }}
            <v-col cols="auto">
              <v-btn @click.prevent="clickDetail(product)" density="compact" icon="mdi-open-in-new"></v-btn>
            </v-col>
          </p>
        </div>
        <!-- 차트 -->
        <div class="chart-container mt-15">
          <canvas id="interestRateChart" width="800" height="400"></canvas>
        </div>
      </div>
      <div v-else class="top-aligned-content">
        <img src="@/assets/question-mark.png" alt="null" width="350" height="350"/>
        <h2 class="mt-10">가입한 상품이 없습니다</h2>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, watch } from 'vue'
import { useUserStore } from '@/stores/users'
import axios from 'axios'
import Chart from 'chart.js/auto'

const userStore = useUserStore()

const products = ref([])
const dialog = ref(false)
const isDeposit = ref(false)

const selectedProduct = ref(null)
const selectedProductCode = ref(null)

const getAllProduct = async () => {
  const deposits = userStore.userContractDeposits
  const savings = userStore.userContractSavings
  let id = 1

  for (const deposit of deposits) {
    const temp = {
      id: id++,
      code: deposit.deposit_code,
      type: '정기예금',
      kor_co_nm: deposit.kor_co_nm,
      fin_prdt_nm: deposit.fin_prdt_nm,
      options: deposit.depositoption_set.map(option => ({
        saveTrm: option.save_trm,
        intr_rate: option.intr_rate,
        intr_rate2: option.intr_rate2
      }))
    }
    products.value.push(temp)
  }

  for (const saving of savings) {
    const temp = {
      id: id++,
      code: saving.saving_code,
      type: '정기적금',
      kor_co_nm: saving.kor_co_nm,
      fin_prdt_nm: saving.fin_prdt_nm,
      options: saving.savingoption_set.map(option => ({
        saveTrm: option.save_trm,
        rsrvTypeNm: option.rsrv_type_nm,
        intr_rate: option.intr_rate,
        intr_rate2: option.intr_rate2
      }))
    }
    products.value.push(temp)
  }
}

// Calculate average interest rate
const calculateAverageInterestRate = (interestRates) => {
  if (interestRates.length === 0) return 0;
  const total = interestRates.reduce((acc, rate) => acc + rate, 0);
  return total / interestRates.length;
};

const closeModal = () => {
  dialog.value = false
}

const clickDetail = (data) => {
  selectedProduct.value = data
  selectedProductCode.value = data.code
  isDeposit.value = data.type === '정기예금'
  getProduct()
  dialog.value = true
}

const getProduct = () => {
  const url = isDeposit.value
    ? `${userStore.API_URL}/finlife/deposit_list/${selectedProductCode.value}/`
    : `${userStore.API_URL}/finlife/saving_list/${selectedProductCode.value}/`

  axios.get(url)
    .then(res => {
      selectedProduct.value = res.data
    })
    .catch(err => {
      console.error(err)
    })
}

const deleteProductUser = async (data) => {
  const answer = window.confirm('가입을 취소하시겠습니까?');
  if (answer) {
    try {
      const url = isDeposit.value
        ? `${userStore.API_URL}/finlife/deposit_list/${selectedProductCode.value}/contract/`
        : `${userStore.API_URL}/finlife/saving_list/${selectedProductCode.value}/contract/`

      await axios.delete(url, {
        headers: {
          Authorization: `Token ${userStore.token}`
        }
      });

      // 서버에서 삭제 후, 로컬 products 리스트에서 제거
      products.value = products.value.filter(product => product.code !== selectedProductCode.value);

      userStore.getUserInfo(userStore.userInfo.username); // 사용자 정보 갱신
      dialog.value = false; // 모달 닫기

      // 삭제 후 차트 다시 그리기
      drawChart();
    } catch (err) {
      console.error(err);
    }
  }
}

let chartInstance = null;

const drawChart = () => {
  const labels = products.value.map(product => product.fin_prdt_nm.length > 10 ? product.fin_prdt_nm.slice(0, 7) + '...' : product.fin_prdt_nm);
  const intrRates = products.value.map(product => parseFloat(product.options[0].intr_rate || 0));
  const avgIntrRate = calculateAverageInterestRate(intrRates);
  const intrRates2 = products.value.map(product => parseFloat(product.options[0].intr_rate2 || 0));
  const avgIntrRate2 = calculateAverageInterestRate(intrRates2);

  const canvas = document.getElementById('interestRateChart');
  if (!canvas) {
    // Canvas element not rendered yet, try again after a short delay
    return setTimeout(drawChart, 100);
  }

  const ctx = canvas.getContext('2d');
  if (!ctx) {
    // Unable to get canvas context, handle error
    console.error('Unable to get canvas context');
    return;
  }

  // If there's a previous chart instance, destroy it
  if (chartInstance) {
    chartInstance.destroy();
  }

  // Create a new chart instance
  chartInstance = new Chart(ctx, {
    type: 'bar',
    data: {
      labels: ['평균 금리', ...labels],
      datasets: [
        {
          label: '저축 금리',
          data: [avgIntrRate, ...intrRates],
          backgroundColor: 'rgba(54, 162, 235, 0.2)',
          borderColor: 'rgba(54, 162, 235, 1)',
          borderWidth: 1
        },
        {
          label: '최고 우대 금리',
          data: [avgIntrRate2, ...intrRates2],
          backgroundColor: 'rgba(255, 99, 132, 0.2)',
          borderColor: 'rgba(255, 99, 132, 1)',
          borderWidth: 1
        }
      ]
    },
    options: {
      // Chart options...
      scales: {
        y: {
          beginAtZero: true
        },
        x: {
          ticks: {
            callback: function(value, index, values) {
              // Truncate long labels
              return this.getLabelForValue(value).length > 10 ? this.getLabelForValue(value).slice(0, 7) + '...' : this.getLabelForValue(value);
            }
          }
        }
      },
      plugins: {
        tooltip: {
          callbacks: {
            title: function(tooltipItem) {
              // Return full label in tooltip
              return products.value[tooltipItem[0].dataIndex - 1]?.fin_prdt_nm; // Use optional chaining to prevent accessing undefined property
            }
          }
        }
      }
    }
  });
};

onMounted(async () => {
  await getAllProduct()
  drawChart(); // 페이지 로드 후 차트 그리기
});

watch(products, () => {
  drawChart(); // 상품 데이터가 변경될 때마다 차트 다시 그리기
});
</script>

<style scoped>
.full-screen-container {
  display: flex;
  flex-direction: column;
  align-items: center;
  padding-top: 20px;
  min-height: 100vh;
  box-sizing: border-box;
  padding-bottom: 20px;
}

h3 {
  margin-bottom: 20px;
}

.content-container {
  display: flex;
  justify-content: center;
  align-items: center;
  width: 100%;
  max-width: 800px;
}

.list-container{
  width: 550px;
  margin: auto;
}

.product-info p {
  margin-bottom: 10px;
}

.product-info {
  padding: 20px;
  border: 1px solid #ccc;
  border-radius: 5px;
  background-color: #f9f9f9;
  max-width: 90%;
  margin: auto;
  margin-bottom: 5px;
}

.product-option-info {
  padding: 20px;
  max-width: 90%;
  margin: auto;
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

.product-item {
  display: flex;
  align-items: center;
  padding: 10px;
  border-bottom: 1px solid #ddd;
}

.product-item span {
  margin-right: 10px;
}

.top-aligned-content {
  display: flex;
  flex-direction: column;
  align-items: center;
}

.chart-container {
  width: 100%;
  max-width: 800px;
  margin-top: 40px;
}
</style>
