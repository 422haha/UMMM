<template>
  <div>
    <div v-if="userInfo" class="d-flex flex-column align-center">
      <div class="profile-img-btn d-flex justify-content-end mb-6">
        <v-btn
          color="#1089FF"
          dark
          rounded
          @click.prevent="editProfileImg"
          class="mt-5"
        >
          <v-icon left>mdi-camera</v-icon>
          프로필 이미지 변경
        </v-btn>
        <v-file-input
          v-show="isShowProfileInput"
          accept="image/png, image/jpeg, image/bmp"
          variant="underlined"
          label="프로필 이미지"
          v-model="image"
          class="mt-4"
        ></v-file-input>
      </div>

      <div class="user-info">
        <v-table>

          <v-dialog v-model="dialog" width="400">
            <v-card>
              <v-card-text>
                <v-text-field
                  type="number"
                  color="#1089FF"
                  variant="outlined"
                  v-model="state.updateValue"
                  :label="selectedKey"
                  :error-messages="v$.updateValue.$errors.map(e => e.$message)"
                  @input="v$.updateValue.$touch"
                  @blur="v$.updateValue.$touch"
                  @keypress.enter="save"
                ></v-text-field>
              </v-card-text>

              <v-card-actions>
                <v-spacer></v-spacer>
                <v-btn color="#1089FF" variant="text" @click="close">
                  취소
                </v-btn>
                <v-btn color="#1089FF" variant="text" @click="save">
                  수정
                </v-btn>
              </v-card-actions>
            </v-card>
          </v-dialog>

          <v-card class="custom-card" v-for="(value, key) in userInfo" :key="key">
            <div class="d-flex justify-content-between align-items-center">
              <v-card-title class="custom-title">{{ key }}</v-card-title>
              <v-card-text class="custom-text">{{ value }}</v-card-text>
              <v-btn v-if="key !== '아이디' && key !== '닉네임' && key !== '이메일'" @click="editValue(key, value)" text color="#1089FF" dark rounded class="mt-1">
                수정
              </v-btn>
            </div>
          </v-card>
        </v-table>
      </div>

    </div>

    <div v-else class="loading">
      <v-progress-circular
        color="#1089FF"
        indeterminate
        size="80"
        ></v-progress-circular>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useUserStore } from '@/stores/users'
import { useVuelidate } from '@vuelidate/core'
import { required, integer, helpers } from '@vuelidate/validators'
import axios from 'axios'

const userInfo = ref()
const dialog = ref(false)
const isShowProfileInput = ref(false)
const image = ref()
const selectedKey = ref('')
const state = ref({
  updateValue: ''
})
const selectedMonth = ref()
const months = [
  { title: '6개월', value: 6 },
  { title: '12개월', value: 12 },
  { title: '24개월', value: 24 },
  { title: '36개월', value: 36 },
]

const userStore = useUserStore()
const usernameTemp = userStore.userInfo.username

const rules = {
  updateValue: {
    required: helpers.withMessage('필수 정보입니다.', required),
    integer: helpers.withMessage('숫자를 입력해야합니다.', integer)
  }
}

const v$ = useVuelidate(rules, state)

onMounted(() => {
  const storeUserInfo = userStore.userInfo
  userInfo.value = {
    '아이디': storeUserInfo.username,
    '닉네임': storeUserInfo.nickname,
    '이메일': storeUserInfo.email,
    '나이': storeUserInfo.age,
    '자산': storeUserInfo.property,
    '연봉': storeUserInfo.annual_salary,
  }
})

const editValue = function (key, value) {
  selectedKey.value = key
  state.value.updateValue = userInfo.value[key]
  selectedMonth.value = value
  dialog.value = true
}

const close = function () {
  dialog.value = false
}

const save = function () {
  v$.value.$validate()

  if (!v$.value.$error) {
    const key = ref('')
    const body = ref(state.value.updateValue)
    if (selectedKey.value === '나이') {
      key.value = 'age'
    } else if (selectedKey.value === '자산') {
      key.value = 'property'
    } else if (selectedKey.value === '연봉') {
      key.value = 'annual_salary'
    }

    axios({
      method: 'put',
      url: `${userStore.API_URL}/users/${usernameTemp}/info/`,
      headers: {
        Authorization: `Token ${userStore.token}`
      },
      data: {
        [key.value]: body.value
      }
    })
      .then((res) => {
        userStore.getUserInfo(usernameTemp)
        userInfo.value[selectedKey.value] = body.value
        selectedKey.value = state.value.updateValue = ''
        selectedMonth.value = null
        dialog.value = false
      })
      .catch((err) => {
        console.log(err)
      })
  }
}

const editProfileImg = function (event) {
  if (isShowProfileInput.value === false) {
    isShowProfileInput.value = true
  } else {
    axios({
      method: 'put',
      url: `${userStore.API_URL}/users/${usernameTemp}/profile/`,
      headers: {
        Authorization: `Token ${userStore.token}`,
        "Content-Type": 'multipart/form-data'
      },
      data: {
        'profile_img': image.value
      }
    })
      .then((res) => {
        userStore.getUserInfo(usernameTemp)
        isShowProfileInput.value = false
      })
      .catch((err) => {
        console.log(err)
      })
  }
}
</script>

<style scoped>
.custom-card {
  width: 500px;
  margin: 10px;
}

.custom-title {
  font-size: 17px;
  width: 100px;
  text-align: center;
}

.custom-text {
  font-size: 17px;
  padding: 0;
  display: flex;
  align-items: center;
}
</style>