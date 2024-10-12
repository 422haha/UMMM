<template>
  <div>
    <img src="@/assets/chatbot.png" @click="toggleChatBot" class="chatbot-icon" />
    <v-dialog v-model="dialog" max-width="500">
      <template v-slot:activator="{ on, attrs }">
        <!-- <v-btn v-bind="attrs" v-on="on">Open Dialog</v-btn> -->
      </template>
      <ChatBot @close="toggleChatBot" />
    </v-dialog>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import ChatBot from '@/components/ChatBot.vue'
import { VDialog, VBtn } from 'vuetify/components'

const dialog = ref(false)

const toggleChatBot = () => {
  dialog.value = !dialog.value
}
</script>

<style scoped>
.chatbot-icon {
  width: 100px;
  height: 100px;
  position: fixed;
  bottom: 30px;
  right: 30px;
  cursor: pointer;
  z-index: 1000;
}
</style>
