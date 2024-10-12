<template>
  <v-container fluid>
    <v-row
    align="center"
    justify="center"
    >
      <v-col
      cols="auto"
      class="btn"
      >
        <v-btn
        :to="{ name: 'depositList' }"
        color="primary"
        class="mr-5"
        outlined
        >
          정기예금
        </v-btn>
        <v-btn
        :to="{ name: 'savingList' }"
        color="primary"
        outlined
        >
          정기적금
        </v-btn>
      </v-col>
    </v-row>
    <RouterView />
  </v-container>
</template>

<script setup>

</script>

<style scoped>
.btn {
  margin-top: 30px;
}
</style>