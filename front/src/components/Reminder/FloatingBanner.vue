<!-- src/pages/FloatingBanner.vue -->
<template>
  <div class="floating-banner-root">
    <div class="banner" :style="bannerStyle" :class="{ blinking }">
      {{ text || '保持心态平稳 · 注意热键 · 记得喝水' }}
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted, onBeforeUnmount } from 'vue'
import { listen } from '@tauri-apps/api/event'
import { register as registerShortcut, unregisterAll } from '@tauri-apps/plugin-global-shortcut'

// 显示文字 & 样式
const text = ref('')
const bannerStyle = ref<Record<string, any>>({})
const blinking = ref(false)
let timerId: number | null = null
let stopId: number | null = null
let blinkAfter = 180
let blinkDuration = 30
let blinkEnabled = true

let unlisten: (() => void) | null = null

function resetTimer() {
  blinking.value = false
  if (timerId) clearTimeout(timerId)
  if (stopId) clearTimeout(stopId)

  if (!blinkEnabled) return

  timerId = window.setTimeout(() => {
    blinking.value = true
    if (blinkDuration > 0) {
      stopId = window.setTimeout(() => {
        blinking.value = false
      }, blinkDuration * 1000)
    }
  }, blinkAfter * 1000)
}

onMounted(async () => {
  // 监听从主窗口发来的事件
  unlisten = await listen('screen-banner:update', (event) => {
    const payload = event.payload as { text: string; style: Record<string, any>; behavior: Record<string, any> }
    text.value = payload.text
    bannerStyle.value = payload.style
    if (payload.behavior) {
    blinkEnabled = !!payload.behavior.blinkEnabled
    blinkAfter = payload.behavior.blinkAfter ?? blinkAfter
    blinkDuration = payload.behavior.blinkDuration ?? blinkDuration
    }
    resetTimer()
  })

  const un2 = await listen('screen-banner:resetBlink', () => {
    resetTimer()
  })
})

onBeforeUnmount(() => {
  unlisten && unlisten()
})
</script>

<style>
.floating-banner-root {
  width: 100%;
}
.banner {
  width: 100%;
  text-align: center;
  border-radius: 10px;
}
.blinking {
  animation: blink 0.8s linear infinite;
}
@keyframes blink {
  0%, 50%, 100% { opacity: 1; }
  25%, 75% { opacity: 0.2; }
}
</style>
