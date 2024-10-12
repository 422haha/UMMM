<template>
  <div class="container-wrapper mt-5">
    <div class="container mt-5">
      <h1>Sign up</h1>
      <form @submit.prevent="signUp" @keypress.enter="signUp" class="mt-7">
        <div style="display: flex; justify-content: space-between;">
          <div class="input-wrapper" style="flex: 1; margin-right: 10px;">
            <div class="text-subtitle-1 text-medium-emphasis">아이디</div>
            <v-text-field
              variant="outlined"
              placeholder="Id"
              v-model="state.username"
              color="primary"
              :error-messages="v$.username.$errors.map(e => e.$message)"
              @input="v$.username.$touch"
              @blur="v$.username.$touch"
            ></v-text-field>
          </div>
          <div class="input-wrapper" style="flex: 1;">
            <div class="text-subtitle-1 text-medium-emphasis">닉네임</div>
            <v-text-field
              variant="outlined"
              placeholder="Nickname"
              v-model="state.nickname"
              color="primary"
              :error-messages="v$.nickname.$errors.map(e => e.$message)"
              @input="v$.nickname.$touch"
              @blur="v$.nickname.$touch"
            ></v-text-field>
          </div>
        </div>
        <div class="text-subtitle-1 text-medium-emphasis">이메일</div>
        <v-text-field
          variant="outlined"
          placeholder="Email"
          v-model="state.email"
          color="primary"
          :error-messages="v$.email.$errors.map(e => e.$message)"
          @input="v$.email.$touch"
          @blur="v$.email.$touch"
          append-inner-icon="mdi-email-outline"
        ></v-text-field>
        <div class="text-subtitle-1 text-medium-emphasis">비밀번호</div>
        <v-text-field
          type="password"
          variant="outlined"
          placeholder="Password"
          v-model="state.password1"
          color="primary"
          @click:append="show1 = !show1"
          :error-messages="v$.password1.$errors.map(e => e.$message)"
          @input="v$.password1.$touch"
          @blur="v$.password1.$touch"
          append-inner-icon="mdi-lock-outline"
        ></v-text-field>
        <div class="text-subtitle-1 text-medium-emphasis">비밀번호 확인</div>
        <v-text-field
          type="password"
          variant="outlined"
          placeholder="Password"
          v-model="state.password2"
          color="primary"
          @click:append="show2 = !show2"
          :error-messages="v$.password2.$errors.map(e => e.$message)"
          @input="v$.password2.$touch"
          @blur="v$.password2.$touch"
          append-inner-icon="mdi-lock-check-outline"
        ></v-text-field>
        <div class="button-wrapper" style="display: flex; justify-content: flex-end;">
          <v-col cols="auto">
          <v-btn @click.prevent="signUp" icon="mdi-login" size="large" color="primary"></v-btn>
          </v-col>
        </div>
      </form>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useUserStore } from '@/stores/users'
import { useVuelidate } from '@vuelidate/core'
import { email, required, minLength, maxLength, alphaNum, sameAs, helpers } from '@vuelidate/validators'

const userStore = useUserStore()

const initialState = {
  username: '',
  nickname: '',
  email: '',
  password1: '',
  password2: '',
}

const state = ref({
  ...initialState
})

const v$ = useVuelidate({
  username: { 
    required: helpers.withMessage('필수 정보입니다.', required),
    alphaNum: helpers.withMessage('영어 대소문자와 숫자만 입력 가능합니다.', alphaNum),
    minLength: helpers.withMessage('5자 이상 입력해 주세요.', minLength(5)),
    maxLength: helpers.withMessage('10자 이하로 입력해 주세요.', maxLength(10))
  },
  nickname: { 
    required: helpers.withMessage('필수 정보입니다.', required),
    maxLength: helpers.withMessage('10자 이하로 입력해 주세요.', maxLength(10))
  },
  email: {
    required: helpers.withMessage('필수 정보입니다.', required),
    email: helpers.withMessage('이메일 주소가 정확한지 확인해 주세요.', email),
    maxLength: helpers.withMessage('30자 이하로 입력해 주세요.', maxLength(30))
  },
  password1: { 
    required: helpers.withMessage('필수 정보입니다.', required),
    minLength: helpers.withMessage('8~16자의 영문 대/소문자, 숫자, 특수문자를 사용해 주세요. 특수문자는 *!@#$%^&만 사용 가능합니다.', minLength(8)),
    maxLength: helpers.withMessage('8~16자의 영문 대/소문자, 숫자, 특수문자를 사용해 주세요. 특수문자는 *!@#$%^&만 사용 가능합니다.', maxLength(16)),
    containspasswordrequirement: helpers.withMessage(
      () => `8~16자의 영문 대/소문자, 숫자, 특수문자를 사용해 주세요. 특수문자는 *!@#$%^&만 사용 가능합니다.`, 
      (value) => /(?=.*[a-z])(?=.*[a-z])(?=.*[0-9])(?=.*[!@#\$%\^&\*])/.test(value)
    )
  },
  password2: { 
    required: helpers.withMessage('필수 정보입니다.', required),
    sameAsPassword: helpers.withMessage('비밀번호가 일치하지 않습니다.', () => sameAs(state.value.password1))
  }
}, state)

const signUp = function () {
  v$.value.$validate()
  if (!v$.value.$error){
    const payload = {
      username: state.value.username,
      nickname: state.value.nickname,
      email: state.value.email,
      password1: state.value.password1,
      password2: state.value.password2,
    }
    userStore.signUp(payload)
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
  width: 600px;
  display: flex;
  flex-direction: column;
  margin: 3rem auto;
  padding: 2rem;
}

.warning {
  color: #b00020;
  font-size: 12px;
}

.button-wrapper {
  margin-top: 1rem;
}
</style>