<template>
  <div>
    <header class="header mt-9">
      <div class="checkboxes">
        <!-- 체크박스 목록 -->
        <!-- 전체 보기 체크박스 -->
        <div class="form-check form-check-inline">
          <input class="form-check-input" type="checkbox" id="allBanks" value="전체 보기" v-model="selectedBank" @change="toggleAllBanks">
          <label class="form-check-label" for="allBanks">전체 보기</label>
        </div>
        <!-- 개별 은행 체크박스 -->
        <div v-for="bank in banks.slice(1)" :key="bank" class="form-check form-check-inline">
          <input class="form-check-input" type="checkbox" :id="bank" :value="bank" v-model="selectedBank" @change="clickBank">
          <label class="form-check-label" :for="bank">{{ bank }}</label>
        </div>
      </div>
    </header>

    <div v-if="savingLength !== 0" class="container mt-3">
      <div class="d-flex flex-row bg-light font-weight-bold py-2">
        <div class="col-6" @click="sortSavings('fin_prdt_nm')">상품명</div>
        <div class="col-6" @click="sortSavings('kor_co_nm')">금융회사명</div>
        <div class="col-3" @click="sortSavings('6month')">6개월</div>
        <div class="col-3" @click="sortSavings('12month')">12개월</div>
        <div class="col-3" @click="sortSavings('24month')">24개월</div>
        <div class="col-3" @click="sortSavings('36month')">36개월</div>
      </div>
      <div v-for="item in filteredSavings" :key="item.saving_code" class="d-flex flex-row py-2 border-bottom" @click="productClick(item)">
        <div class="col-6">{{ item.fin_prdt_nm }}</div>
        <div class="col-6">{{ item.kor_co_nm }}</div>
        <div class="col-3">{{ item['6month'] }}</div>
        <div class="col-3">{{ item['12month'] }}</div>
        <div class="col-3">{{ item['24month'] }}</div>
        <div class="col-3">{{ item['36month'] }}</div>
      </div>
    </div>
    <div v-else class="container mt-3">
      <div class="alert alert-info" role="alert">
        조회된 정기예금 상품이 없습니다.
      </div>
    </div>
    <!-- 모달 -->
    <v-dialog v-model="dialog" width="900">
      <template #activator="{ on }">
        <!-- 활성화자로 사용할 버튼 또는 요소 -->
      </template>
      <!-- 모달 내용 -->
      <v-card v-if="selectedSaving" class="py-5 px-3">
        <v-card-title class="d-flex align-center justify-space-between">
          <div class="d-flex">
            <v-icon color="#FFC107" icon="mdi-piggy-bank-outline"></v-icon>
            <h3 class="ml-3">{{ selectedSaving['fin_prdt_nm'] }}</h3>
          </div> 
          <div v-if="userStore.isLogin">
            <v-btn
              v-if="isContractSaving"
              color="red"
              variant="flat"
              @click.prevent="deleteSavingUser"
            >가입 취소하기</v-btn>
            <v-btn
              v-else
              color="#1089FF"
              variant="flat"
              @click.prevent="addSavingUser"
            >가입하기</v-btn>
          </div>
        </v-card-title>
        <div class="mt-5">
          <div class="saving-info">
            <p><strong>금융 회사명 :</strong> {{ selectedSaving.kor_co_nm || '정보 없음' }}</p>
            <p><strong>가입 방법 :</strong> {{ selectedSaving.join_way || '정보 없음' }}</p>
            <p><strong>만기 후 이자율 :</strong> {{ selectedSaving.mtrt_int || '정보 없음' }}</p>
            <p><strong>우대 조건 :</strong> {{ selectedSaving.spcl_cnd || '정보 없음' }}</p>
            <p><strong>가입 제한 :</strong> {{ selectedSaving.join_deny === 1 ? '가입 가능' : selectedSaving.join_deny === 2 ? '서민 전용': '일부 제한' }}</p>
            <p><strong>가입 대상 :</strong> {{ selectedSaving.join_member || '정보 없음' }}</p>
            <p><strong>기타 사항 :</strong> {{ selectedSaving.etc_note || '정보 없음' }}</p>
            <p><strong>최고 한도 :</strong> {{ selectedSaving.max_limit || '정보 없음' }}</p>
          </div>
          <div class="saving-option-info">
            <p class="mb-4"><strong>금융 상품 옵션</strong></p>
            <div class="options-container">
              <div v-for="(option, index) in selectedSaving.options" :key="index" class="option-card">
                <p><strong>이자율 유형 :</strong> {{ option.rsrv_type_nm || '정보 없음' }}</p>
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
  </div>
</template>

<script setup>
import { ref, onMounted, computed } from 'vue'
import { useUserStore } from '@/stores/users'
import axios from 'axios'
import { useRouter } from 'vue-router'

const headers = [
  { title: '금융회사명', align: 'start', sortable: true, key: 'kor_co_nm' },
  { title: '상품명', align: 'center', sortable: true, width: '32%', key: 'fin_prdt_nm' },
  { title: '6개월 (Click to sort)', align: 'end', width: '12%', key: '6month' },
  { title: '12개월 (Click to sort)', align: 'end', width: '12%', key: '12month' },
  { title: '24개월 (Click to sort)', align: 'end', width: '12%', key: '24month' },
  { title: '36개월 (Click to sort)', align: 'end', width: '12%', key: '36month' },
]

const savings = ref([])
const savingLength = computed(() => savings.value.length)
const banks = ref(['전체 보기'])
const selectedBank = ref(['전체 보기']) // 배열로 초기화
const selectedSaving = ref()
const selectedSavingSimple = ref()
const selectedSavingCode = computed(() => {
  return selectedSavingSimple.value?.['saving_code']
})
const dialog = ref(false)
const sortColumn = ref(null)
const sortDirection = ref('asc') // 기본 정렬 방향은 오름차순

const userStore = useUserStore()
const router = useRouter()

const makeItems = function (item) {
  const result = {
    saving_code: item.saving_code,
    kor_co_nm: item.kor_co_nm,
    fin_prdt_nm: item.fin_prdt_nm,
    '6month': null,
    '12month': null,
    '24month': null,
    '36month': null,
  }

  for (const option of item.savingoption_set) {
    const saveTrm = option.save_trm

    if (saveTrm === '6') {
      result['6month'] = option.intr_rate
    } else if (saveTrm === '12') {
      result['12month'] = option.intr_rate
    } else if (saveTrm === '24') {
      result['24month'] = option.intr_rate
    } else if (saveTrm === '36') {
      result['36month'] = option.intr_rate
    }
  }

  return result
}

const getAllSaving = function () {
  axios({
    method: 'get',
    url: `${userStore.API_URL}/finlife/saving_list/`,
  })
    .then((res) => {
      savings.value = []; // 데이터 초기화
      const results = res.data;
      for (const item of results) {
        savings.value.push(makeItems(item));
        if (!banks.value.includes(item.kor_co_nm)) {
          banks.value.push(item.kor_co_nm);
        }
      }
    })
    .catch((err) => {
      console.log(err);
    });
};

onMounted(() => {
  getAllSaving()
})

const toggleAllBanks = function () {
  if (selectedBank.value.includes('전체 보기')) {
    selectedBank.value = ['전체 보기']
  } else {
    selectedBank.value = []
  }
}

const sortSavings = function (key) {
  if (sortColumn.value === key) {
    // 클릭된 열이 이미 정렬된 열인 경우, 정렬 방향을 변경합니다.
    sortDirection.value = sortDirection.value === 'asc' ? 'desc' : 'asc'
  } else {
    // 클릭된 열이 정렬되지 않은 새로운 열인 경우, 정렬 열을 변경하고 오름차순으로 설정합니다.
    sortColumn.value = key
    sortDirection.value = 'asc'
  }

  // 정렬 방향에 따라 정렬합니다.
  savings.value.sort((a, b) => {
    const aValue = a[key] === null ? Number.NEGATIVE_INFINITY : a[key]
    const bValue = b[key] === null ? Number.NEGATIVE_INFINITY : b[key]

    // 오름차순으로 정렬합니다.
    if (sortDirection.value === 'asc') {
      if (aValue < bValue) return -1
      if (aValue > bValue) return 1
      return 0
    } else {
      // 내림차순으로 정렬합니다.
      if (aValue < bValue) return 1
      if (aValue > bValue) return -1
      return 0
    }
  })
}

const productClick = function (data) {
  if (data) {
    selectedSavingSimple.value = data
    getSaving()
    dialog.value = true  // 모달 표시
  }
}

const filteredSavings = computed(() => {
  // 전체 보기를 선택한 경우 모든 정기적금 상품 반환
  if (selectedBank.value.includes('전체 보기')) {
    return savings.value
  }
  // 선택한 은행에 해당하는 정기적금 상품만 필터링하여 반환
  return savings.value.filter(item => selectedBank.value.includes(item.kor_co_nm))
})

const closeModal = function () {
  dialog.value = false;
}

const isContractSaving = computed(() => {
  return userStore.userInfo?.contract_saving.some(e => e['saving_code'] === selectedSavingCode.value)
})

const getSaving = function () {
  const savingCode = selectedSavingSimple.value['saving_code']
  axios({
    method: 'get',
    url: `${userStore.API_URL}/finlife/saving_list/${selectedSavingCode.value}/`,
  })
    .then((res) => {
      const data = res.data
      selectedSaving.value = res.data
    })
    .catch((err) => {
      console.log(err)
    })
}

// 가입하기 함수
const addSavingUser = function () {
  axios({
    method: 'post',
    url: `${userStore.API_URL}/finlife/saving_list/${selectedSavingCode.value}/contract/`,
    headers: {
      Authorization: `Token ${userStore.token}`
    }
  })
    .then((res) => {
      // 가입이 성공하면 사용자에게 피드백을 제공하고 필요한 작업을 수행
      alert('저장이 완료되었습니다.')
      // 필요하다면 사용자의 정보를 업데이트
      userStore.getUserInfo(userStore.userInfo.username)
      // 사용자에게 확인 메시지를 보여주고, 가입 상품 관리 페이지로 이동할지 물어봄
      const answer = window.confirm('가입이 완료되었습니다. 가입 상품 관리 페이지로 이동하시겠습니까?')
      if (answer) {
        router.push({ name: 'productManage', params: { username: userStore.userInfo.username }})
      }
    })
    .catch((err) => {
      console.log(err)
      // 에러 발생 시 적절한 처리를 수행
    })
}

// 가입 취소하기 함수
const deleteSavingUser = function () {
  axios({
    method: 'delete',
    url: `${userStore.API_URL}/finlife/saving_list/${selectedSavingCode.value}/contract/`,
    headers: {
      Authorization: `Token ${userStore.token}`
    }
  })
    .then((res) => {
      // 가입 취소가 성공하면 필요한 작업을 수행
      // 필요하다면 사용자의 정보를 업데이트
      userStore.getUserInfo(userStore.userInfo.username)
    })
    .catch((err) => {
      console.log(err)
      // 에러 발생 시 적절한 처리를 수행
    })
}
</script>


<style scoped>
.header {
  padding: 1rem;
  background-color: #f8f9fa;
  border-bottom: 1px solid #dee2e6;
  margin-bottom: 20px;
}

.checkboxes {
  display: flex;
  flex-wrap: wrap;
  gap: 10px;
}

.container {
  width: 100%;
}

.bg-light {
  background-color: #f8f9fa !important;
}

.font-weight-bold {
  font-weight: 700;
}

.border-bottom {
  border-bottom: 1px solid #dee2e6 !important;
}

.col-6 {
  flex: 0 0 25%;
  max-width: 25%;
}

.col-3 {
  flex: 0 0 12.5%;
  max-width: 12.5%;
}

.saving-info p {
  margin-bottom: 10px;
}

.saving-info {
  padding: 20px;
  border: 1px solid #ccc;
  border-radius: 5px;
  background-color: #f9f9f9;
  max-width: 90%;
  margin: auto;
  margin-bottom: 5px;
}

.saving-option-info {
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
    flex: 0 0 calc(33.333% - 15px); /* 3개씩 배치하고, 카드 사이 간격을 위해 20px 차감 */
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