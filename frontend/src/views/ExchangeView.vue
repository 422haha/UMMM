<template>
  <v-container class="d-flex justify-center align-center mt-15">
    <v-form class="exchange-form d-flex flex-column justify-center align-center">
      <v-select
        :items="states"
        label="기준"
        v-model="selectedState"
        variant="underlined"
      ></v-select>
      <v-select
        label="통화 선택"
        :items="currencies"
        v-model="selectedCurrency"
        variant="underlined"
      ></v-select>
      <v-text-field
        type="number"
        prepend-icon="$vuetify"
        :label="selectedCurrencyUnit"
        v-model="otherInput"
        @input="inputEventOther"
        color="primary"
        clearable
      ></v-text-field>
      <v-text-field
        type="number"
        prepend-icon="$vuetify"
        append-inner-icon="mdi-currency-krw"
        label="KRW"
        v-model="krwInput"
        @input="inputEventKrw"
        color="primary"
      ></v-text-field>
    </v-form>
  </v-container>
</template>

<script setup>
import { ref, onMounted, watch } from 'vue'
import { useUserStore } from '@/stores/users'
import axios from 'axios'

const datas = ref([])
const currencies = ref()
const response = ref()
const selectedState = ref('송금 받을때')
const selectedCurrency = ref('미국 달러')
const selectedCurrencyUnit = ref('USD')
const selectedTtb = ref()   // 송금 받을때
const selectedTts = ref()   // 송금 보낼때
const selectedDeal = ref()  // 매매기준율

const calculateVariable = ref()
const krwInput = ref()
const otherInput = ref()

const states = ['송금 받을때', '송금 보낼때', '매매기준율']

const userStore = useUserStore()

const emit = defineEmits(['passCurrency'])

onMounted(() => {
  axios({
    method: 'get',
    url: `${userStore.API_URL}/exchange/`
  }).then((res) => {
    response.value = res.data.filter(data => data['ttb'] !== '0')
    currencies.value = response.value.map(item => item['cur_nm'])
    const units = response.value.map(item => item['cur_unit'])
    emit('passCurrency', currencies.value, units)
    const usdInfo = response.value.find(item => item['cur_nm'] === '미국 달러')
    selectedTtb.value = Number(usdInfo['ttb'].replaceAll(',', ''))
    selectedTts.value = Number(usdInfo['tts'].replaceAll(',', ''))
    selectedDeal.value = Number(usdInfo['deal_bas_r'].replaceAll(',', ''))
    calculateVariable.value = selectedTtb.value
  })
})

watch(selectedCurrency, () => {
  const selectedInfo = response.value.find(item => item['cur_nm'] === selectedCurrency.value)
  selectedCurrencyUnit.value = selectedInfo['cur_unit']
  if (selectedCurrency.value === '일본 옌' || selectedCurrency.value === "인도네시아 루피아") {
    selectedCurrencyUnit.value = selectedCurrencyUnit.value.replace('(100)', '')
    selectedTtb.value = Number(selectedInfo['ttb'].replaceAll(',', '')) / 100
    selectedTts.value = Number(selectedInfo['tts'].replaceAll(',', '')) / 100
    selectedDeal.value = Number(selectedInfo['deal_bas_r'].replaceAll(',', '')) / 100
  } else {
    selectedTtb.value = Number(selectedInfo['ttb'].replaceAll(',', ''))
    selectedTts.value = Number(selectedInfo['tts'].replaceAll(',', ''))
    selectedDeal.value = Number(selectedInfo['deal_bas_r'].replaceAll(',', ''))
  }
  if (selectedState.value === '송금 받을때') {
    calculateVariable.value = selectedTtb.value
  } else if (selectedState.value === '송금 보낼때') {
    calculateVariable.value = selectedTts.value
  } else {
    calculateVariable.value = selectedDeal.value
  }
  inputEventOther()
})

watch(selectedState, () => {
  if (selectedState.value === '송금 받을때') {
    calculateVariable.value = selectedTtb.value
  } else if (selectedState.value === '송금 보낼때') {
    calculateVariable.value = selectedTts.value
  } else {
    calculateVariable.value = selectedDeal.value
  }
  inputEventOther()
})

const roundToTwo = (num) => {
  return +(Math.round(num + 'e+2') + 'e-2')
}

const inputEventKrw = function () {
  otherInput.value = krwInput.value / calculateVariable.value
  otherInput.value = roundToTwo(otherInput.value)
}

const inputEventOther = function () {
  krwInput.value = otherInput.value * calculateVariable.value
  krwInput.value = roundToTwo(krwInput.value)
}

const passCurrency = function (cur, uni) {
  datas.value = []
  for (let i=0; i < cur.length; i++) {
    if (uni[i].includes('(100)')) {
      datas.value.push({ 'cur': cur[i], 'unit': uni[i].slice(0, 3) })
    } else if (uni[i] !== 'CNH')  {
      datas.value.push({ 'cur': cur[i], 'unit': uni[i] })
    }
  }
}
</script>

<style scoped>
.exchange-form {
  max-width: 600px;
  width: 100%;
  padding: 20px;
  border: 1px outset #007bff;
  border-radius: 10px;
  box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
}

.v-select,
.v-text-field {
  margin-top: 20px;
  margin-bottom: 5px;
  width: 90%;
}
</style>