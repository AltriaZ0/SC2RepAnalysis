<!-- src/components/Home/UpdateHistory.vue -->
<template>
  <div class="article-container">
    <div v-if="loading" class="loading">加载中...</div>
    <div v-else-if="error" class="error">{{ error }}</div>
    <div v-else class="article-content" v-html="htmlContent"></div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { marked } from 'marked'

const loading = ref(true)
const error = ref<string | null>(null)
const htmlContent = ref('')

onMounted(async () => {
  try {
    const response = await fetch('/articles/updatehistory.md')
    if (!response.ok) {
      throw new Error(`HTTP ${response.status}: ${response.statusText}`)
    }
    const markdownText = await response.text()
    htmlContent.value = marked(markdownText, {
      breaks: true,
      gfm: true
    })
  } catch (err) {
    console.error('加载更新日志失败:', err)
    error.value = '无法加载更新日志，请稍后重试。'
  } finally {
    loading.value = false
  }
})
</script>

<style scoped>
.article-container {
  background-color: #1a1a1a;
  border-radius: 8px;
  padding: 16px;
  margin-bottom: 16px;
  color: #e0e0e0;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.3);
}

.loading, .error {
  text-align: center;
  padding: 40px;
}

.article-content {
  line-height: 1.6;
  font-size: 16px;
}
.article-content h1 { font-size: 2rem; margin: 1.5rem 0 1rem; }
.article-content h2 { font-size: 1.5rem; margin: 1.2rem 0 0.8rem; }
.article-content p { margin: 1rem 0; }
.article-content code {
  background: #2d2d2d;
  padding: 2px 6px;
  border-radius: 4px;
}
.article-content pre {
  background: #2d2d2d;
  padding: 12px;
  border-radius: 6px;
  overflow-x: auto;
}
</style>