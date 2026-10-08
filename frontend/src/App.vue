<template>
  <router-view />
  <button
    v-if="showBackButton"
    class="global-back-btn"
    type="button"
    @click="goBack"
  >
    Back
  </button>
</template>

<script setup>
import { computed } from "vue"
import { useRoute, useRouter } from "vue-router"

const route = useRoute()
const router = useRouter()

const showBackButton = computed(() => route.path !== "/")

const goBack = () => {
  if (window.history.length > 1) {
    router.back()
    return
  }
  router.push("/")
}
</script>

<style scoped>
.global-back-btn {
  position: fixed;
  left: 20px;
  bottom: 20px;
  z-index: 1200;
  border: none;
  border-radius: 999px;
  padding: 0.6rem 1.1rem;
  background: rgba(15, 23, 42, 0.9);
  color: #fff;
  font-weight: 600;
  cursor: pointer;
  box-shadow: 0 10px 24px rgba(15, 23, 42, 0.22);
}

.global-back-btn:hover {
  background: #0f172a;
}
</style>
